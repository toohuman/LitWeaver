import cyclopts
import logging
from pathlib import Path

# Use relative imports to access other parts of your package
from .project_manager import create_new_project, get_project_paths
from .document_processing import process_pdfs_in_directory
from .config import load_config # Example
# from .workflows import run_interactive_query # Example for later

# Setup logging (configure more robustly later)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create the main Cyclopts application object
app = cyclopts.App(help="LitWeaver: Your AI Research Assistant for Literature Reviews")

@app.command
def init(
    project_name: str,
    base_dir: Path = Path("projects") # Allow overriding base project dir
):
    """
    Initialises a new LitWeaver project directory structure.
    Creates 'projects/[project_name]/papers/'.
    """
    try:
        project_paths = create_new_project(project_name, base_dir)
        print(f"Project '{project_name}' initialised successfully.")
        print(f"  - Project Root: {project_paths['root']}")
        print(f"  - Papers Dir:   {project_paths['papers']}")
        print(f"  - Vector Store: {project_paths['vector_store']}")
        print(f"\nPlease add your PDF papers to the '{project_paths['papers'].relative_to(Path.cwd())}' directory.")
    except FileExistsError as e:
        print(f"Error: {e}")
    except Exception as e:
        logging.error(f"Failed to initialize project {project_name}: {e}", exc_info=True)
        print(f"An unexpected error occurred during initialisation. Check logs.")

@app.command
def process(
    project_name: str,
    base_dir: Path = Path("projects")
):
    """
    Finds PDFs in the project's 'papers' directory, processes them,
    and builds/updates the vector store.
    """
    try:
        paths = get_project_paths(project_name, base_dir)
        print(f"Processing PDFs for project '{project_name}'...")
        # Delegate the actual processing logic
        processed_count, chunk_count = process_pdfs_in_directory(
            papers_dir=paths['papers'],
            vector_store_path=paths['vector_store']
            # Pass embedding model, chunking config etc. here or load from config
        )
        if processed_count is not None:
            print(f"\nProcessing complete.")
            print(f"  - Successfully processed {processed_count} PDF file(s).")
            print(f"  - Added/Updated {chunk_count} chunks in the vector store at: {paths['vector_store']}")
        else:
            print("Processing finished, but no files were processed or an issue occurred.") # Or handle errors better

    except FileNotFoundError as e:
        print(f"Error: Project directory or papers directory not found for '{project_name}'. {e}")
        print(f"Did you run 'litweaver init {project_name}' first?")
    except Exception as e:
        logging.error(f"Failed to process PDFs for project {project_name}: {e}", exc_info=True)
        print(f"An unexpected error occurred during processing. Check logs.")

# --- Placeholder for future interactive command ---
# @app.command
# def query(project_name: str, query_text: str):
#     """Queries the project's literature base."""
#     # print(f"Querying '{project_name}' with: {query_text}")
#     # result = run_interactive_query(project_name, query_text)
#     # print("Response:", result)
#     pass

# It's good practice to have a main function if this file might be run directly
# but the entry point in pyproject.toml makes this less critical for installation.
# def main():
#    app()

# if __name__ == "__main__":
#    main()