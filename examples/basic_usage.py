"""Basic usage examples for the GLEIF API client."""

from gleif_mcp.client import GleifClient

def main():
    """Main function to demonstrate basic usage."""
    client = GleifClient()

    print("--- Get LEI Record ---")
    try:
        record = client.get_lei_record("529900T8BM49AURSDO55")
        print(f"Successfully retrieved record for: {record.get('entity', {}).get('legalName', {}).get('name')}")
    except Exception as e:
        print(f"Error retrieving record: {e}")

    print("\n--- Search for LEI Records ---")
    try:
        results = client.search_by_name("Apple")
        print(f"Found {len(results)} records for 'Apple':")
        for entity in results[:5]:
            print(f"  - {entity.get('lei')}: {entity.get('entity', {}).get('legalName', {}).get('name')}")
    except Exception as e:
        print(f"Error searching for records: {e}")

if __name__ == "__main__":
    main()

