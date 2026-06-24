import os
import json
from groww_pulse.config import load_config
from groww_pulse.ingestion import ingest_reviews
from groww_pulse.summarizer import Summarizer

def main():
    # Load config
    print("Loading config...")
    config = load_config()
    
    # Phase 1: Ingestion
    print("\n--- Phase 1: Ingestion ---")
    reviews = ingest_reviews(config)
    print(f"Ingested {len(reviews)} reviews.")
    
    if not reviews:
        print("No reviews to process. Exiting.")
        return
        
    from groww_pulse.clustering import generate_embeddings, perform_clustering, rank_and_build_clusters
    
    # Phase 2: Clustering
    print("\n--- Phase 2: Clustering ---")
    print("Generating embeddings...")
    embeddings = generate_embeddings(reviews, config.clustering)
    
    print("Performing clustering...")
    labels = perform_clustering(embeddings, config.clustering)
    
    print("Ranking and building clusters...")
    clusters = rank_and_build_clusters(reviews, labels, embeddings)
    print(f"Generated {len(clusters)} clusters.")
    
    # Phase 3: LLM Summarization
    print("\n--- Phase 3: Summarization (LLM) ---")
    summarizer = Summarizer(config.llm)
    
    summaries = []
    for i, cluster in enumerate(clusters):
        print(f"Summarizing Cluster {cluster.cluster_id} ({cluster.size} reviews)...")
        summary = summarizer.summarize_cluster(cluster)
        if summary:
            summaries.append(summary.model_dump())
            print(f" -> Theme: {summary.theme_name}")
            print(f" -> Description: {summary.description}")
        else:
            print(" -> Failed to summarize.")
            
    # Save the output
    os.makedirs("data", exist_ok=True)
    out_file = "data/phase3_output.json"
    with open(out_file, "w") as f:
        json.dump(summaries, f, indent=2)
    print(f"\nSaved {len(summaries)} summaries to {out_file}")

    # Phase 4: Rendering
    print("\n--- Phase 4: Rendering ---")
    from groww_pulse.renderer import render_google_doc_content, render_email_payload
    from groww_pulse.summarizer import ThemeSummary
    
    # Re-hydrate pydantic models for rendering
    theme_summaries = [ThemeSummary(**s) for s in summaries]
    iso_week = "2026-W24" # Mock week for now
    
    doc_content = render_google_doc_content(theme_summaries, iso_week, config)
    doc_file = "data/rendered_doc.md"
    with open(doc_file, "w") as f:
        f.write(doc_content)
    print(f"Saved rendered Google Doc markdown to {doc_file}")
    
    email_payload = render_email_payload(theme_summaries, iso_week, config, "https://docs.google.com/document/d/mock")
    email_file = "data/rendered_email.html"
    with open(email_file, "w") as f:
        f.write(email_payload.html_body)
    print(f"Saved rendered Email HTML to {email_file}")

if __name__ == "__main__":
    main()
