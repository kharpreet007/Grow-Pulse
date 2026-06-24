import click
from .config import load_config
from datetime import datetime
from groww_pulse.receipts import ReceiptManager, RunReceipt, DeliveryStatus

@click.group()
def cli():
    pass

@cli.command()
@click.option('--week', default=None, help='ISO week to get status for')
@click.option('--all', 'show_all', is_flag=True, default=False, help='Show all receipts')
def status(week, show_all):
    config = load_config()
    manager = ReceiptManager(config.receipts.storage_path)
    
    if show_all:
        receipts = manager.get_all_receipts()
        if not receipts:
            click.secho("No receipts found.", fg="yellow")
            return
        for w, r in receipts.items():
            click.secho(f"Week {w}: Status {r.status}", fg="green" if r.status == "success" else "yellow")
    else:
        if not week:
            current_date = datetime.now()
            year, current_week, _ = current_date.isocalendar()
            week = f"{year}-W{current_week:02d}"
        
        receipt = manager.load_receipt(week)
        if not receipt:
            click.secho(f"No receipt found for week {week}", fg="yellow")
        else:
            import json
            click.secho(json.dumps(receipt.to_dict(), indent=2), fg="cyan")

@cli.command()
@click.option('--week', default=None, help='ISO week to generate the report for (e.g. 2026-W24)')
@click.option('--window', type=int, default=None, help='Rolling window in weeks for review ingestion')
@click.option('--dry-run', is_flag=True, default=False, help='Run pipeline but skip delivery (no Doc/Gmail writes)')
@click.option('--draft-only', is_flag=True, default=False, help='Create Gmail draft but do not send')
@click.option('--use-cache', is_flag=True, default=False, help='Skip phases 1-3 and load summaries from data/phase3_output.json')
def run(week, window, dry_run, draft_only, use_cache):
    config = load_config()
    # Override config with CLI arguments if needed
    if draft_only:
        config.delivery.draft_only = True
    if window:
        config.ingestion.window_weeks = window
    
    # Generate ISO week string if not provided
    if not week:
        current_date = datetime.now()
        year, current_week, _ = current_date.isocalendar()
        week = f"{year}-W{current_week:02d}"

    click.secho(f"=== Groww Review Pulse ===", fg="cyan", bold=True)
    click.secho(f"Week: {week}", fg="cyan")
    click.secho(f"Window: {config.ingestion.window_weeks} weeks", fg="cyan")
    click.secho(f"Dry Run: {dry_run}", fg="cyan")
    click.secho(f"Draft Only: {config.delivery.draft_only}", fg="cyan")
    click.secho(f"Use Cache: {use_cache}", fg="cyan")
    click.secho(f"App ID: {config.product.play_store_app_id}", fg="cyan")
    click.secho("==========================", fg="cyan", bold=True)
    
    manager = ReceiptManager(config.receipts.storage_path)
    receipt = manager.load_receipt(week)
    
    if not receipt:
        receipt = RunReceipt(
            iso_week=week,
            timestamp=datetime.now().isoformat(),
            status="pending",
            delivery=DeliveryStatus(docs_status="pending", gmail_status="pending")
        )
    
    summaries = []
    reviews_ingested = 0
    clusters_found = 0
    
    if use_cache:
        import json
        from groww_pulse.summarizer import ThemeSummary
        click.secho("\n--- Using Cache (Skipping Phases 1-3) ---", fg="magenta")
        try:
            with open("data/phase3_output.json", "r") as f:
                data = json.load(f)
                summaries = [ThemeSummary(**s) for s in data]
            click.secho(f"Loaded {len(summaries)} summaries from cache.", fg="green")
            themes_generated = len(summaries)
        except Exception as e:
            click.secho(f"Failed to load cache: {e}", fg="red")
            return
    else:
        # Phase 1: Ingestion
        click.secho("\n--- Phase 1: Ingestion ---", fg="magenta")
        from groww_pulse.ingestion import ingest_reviews
        reviews = ingest_reviews(config)
        reviews_ingested = len(reviews)
        click.secho(f"Ingested {reviews_ingested} reviews.", fg="green")
        
        if not reviews:
            click.secho("No reviews to process. Exiting.", fg="yellow")
            receipt.status = "failed"
            receipt.error = "0 reviews ingested"
            manager.save_receipt(receipt)
            return
            
        # Phase 2: Clustering
        click.secho("\n--- Phase 2: Clustering ---", fg="magenta")
        from groww_pulse.clustering import generate_embeddings, perform_clustering, rank_and_build_clusters
        click.secho("Generating embeddings...", fg="cyan")
        embeddings = generate_embeddings(reviews, config.clustering)
        
        click.secho("Performing clustering...", fg="cyan")
        labels = perform_clustering(embeddings, config.clustering)
        
        click.secho("Ranking and building clusters...", fg="cyan")
        clusters = rank_and_build_clusters(reviews, labels, embeddings)
        clusters_found = len(clusters)
        click.secho(f"Generated {clusters_found} clusters.", fg="green")
        
        if clusters_found == 0:
            click.secho("No clusters found. Exiting.", fg="yellow")
            receipt.status = "failed"
            receipt.error = "0 clusters found"
            manager.save_receipt(receipt)
            return
            
        # Phase 3: LLM Summarization
        click.secho("\n--- Phase 3: Summarization (LLM) ---", fg="magenta")
        from groww_pulse.summarizer import Summarizer
        summarizer = Summarizer(config.llm)
        
        for i, cluster in enumerate(clusters):
            click.secho(f"Summarizing Cluster {cluster.cluster_id} ({cluster.size} reviews)...", fg="cyan")
            try:
                summary = summarizer.summarize_cluster(cluster)
                if summary:
                    summaries.append(summary)
                    click.secho(f" -> Theme: {summary.theme_name}", fg="green")
                else:
                    click.secho(" -> Failed to summarize.", fg="red")
            except Exception as e:
                click.secho(f" -> LLM Error: {e}", fg="red")
                receipt.status = "partial"
                receipt.error = f"LLM Error: {e}"
                manager.save_receipt(receipt)
                return
                
        if not summaries:
            click.secho("No summaries generated. Exiting.", fg="yellow")
            receipt.status = "failed"
            receipt.error = "0 summaries generated"
            manager.save_receipt(receipt)
            return
            
    receipt.reviews_ingested = reviews_ingested
    receipt.clusters_found = clusters_found
    receipt.themes_generated = len(summaries)
    
    # Phase 4: Rendering
    click.secho("\n--- Phase 4: Rendering ---", fg="magenta")
    from groww_pulse.renderer import render_google_doc_content, render_email_payload
    
    doc_content = render_google_doc_content(summaries, week, config)
    
    doc_id = getattr(config.delivery, 'google_doc_id', 'YOUR_DOC_ID')
    doc_link = f"https://docs.google.com/document/d/{doc_id}/edit"
    email_payload = render_email_payload(summaries, week, config, doc_link)
    
    if dry_run:
        click.secho("\n[DRY RUN] Rendering complete. Skipping delivery.", fg="yellow")
        return
        
    # Phase 4: Delivery
    click.secho("\n--- Phase 4: Delivery ---", fg="magenta")
    from groww_pulse.delivery import append_to_google_doc, deliver_email
    
    if receipt.delivery.docs_status == "appended":
        click.secho(f"Skipping Google Doc append. Already appended according to receipt.", fg="yellow")
    else:
        click.secho("Appending to Google Doc...", fg="cyan")
        try:
            doc_res = append_to_google_doc(doc_content, config)
            click.secho(f"Doc append success: {doc_res}", fg="green")
            receipt.delivery.docs_status = "appended"
            receipt.delivery.docs_id = doc_id
            manager.save_receipt(receipt)
        except Exception as e:
            click.secho(f"Doc append failed: {e}", fg="red")
            receipt.delivery.docs_status = "failed"
            receipt.status = "failed"
            receipt.error = str(e)
            manager.save_receipt(receipt)
            click.secho("Aborting email delivery because Docs failed.", fg="red")
            return
            
    # Email Delivery idempotency check
    if receipt.delivery.gmail_status in ("sent", "drafted"):
        click.secho(f"Skipping Email Delivery. Already {receipt.delivery.gmail_status} according to receipt.", fg="yellow")
    else:
        click.secho(f"Sending Email (Draft Only: {config.delivery.draft_only})...", fg="cyan")
        try:
            email_res = deliver_email(email_payload, config.delivery.draft_only, config)
            click.secho(f"Email delivery success: {email_res}", fg="green")
            
            receipt.delivery.gmail_draft_id = email_res.get("draft_id")
            if config.delivery.draft_only or email_res.get("message_id") is None:
                receipt.delivery.gmail_status = "drafted"
            else:
                receipt.delivery.gmail_status = "sent"
                receipt.delivery.gmail_message_id = email_res.get("message_id")
                
            receipt.status = "success"
            manager.save_receipt(receipt)
        except Exception as e:
            click.secho(f"Email delivery failed: {e}", fg="red")
            receipt.delivery.gmail_status = "failed"
            receipt.status = "partial" # doc succeeded, email failed
            receipt.error = str(e)
            manager.save_receipt(receipt)
            return
            
    click.secho("\nPipeline finished successfully!", fg="green", bold=True)
    click.secho(f"Receipt saved at: {manager._get_receipt_path(receipt.iso_week)}", fg="cyan")

if __name__ == "__main__":
    cli()
