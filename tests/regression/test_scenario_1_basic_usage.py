"""Executable walkthrough for `scenario_1_basic_usage.md`.
Run `python docs/examples/scenario_1_basic_usage.py` to exercise every code
sample from the Scenario 1 documentation in a single pass.
"""
import os

from typing import Any, Dict, Optional
from dotenv import load_dotenv
from powermem import create_memory

# Check if .env exists and load it
env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
env_example_path = os.path.join(os.path.dirname(__file__), "..", "..", "env.example")

if not os.path.exists(env_path):
    print(f"\n No .env file found at: {env_path}")
    print(f"To add your API keys:")
    print(f"   1. Copy: cp {env_example_path} {env_path}")
    print(f"   2. Edit {env_path} and add your API keys")
    print(f"\n  For now, using mock providers for demonstration...")
else:
    print(f"Found .env file")
    # Explicitly load configs/.env file
    load_dotenv(env_path, override=True)
    


def _print_banner(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def _print_step(title: str) -> None:
    print("\n" + "-" * 60)
    print(title)
    print("-" * 60)


def _get_results_list(result: Any) -> list[Dict[str, Any]]:
    if isinstance(result, dict):
        results = result.get("results")
        if isinstance(results, list):
            return results
    return []


def _extract_memory_id(result: Any) -> Optional[int]:
    results = list(_get_results_list(result))
    if not results:
        return None
    first = results[0]
    if isinstance(first, dict):
        memory_id = first.get("id") or first.get("memory_id")
        if isinstance(memory_id, (int, str)):
            try:
                return int(memory_id)
            except (TypeError, ValueError):
                return None
    return None


def _memory_text(entry: Dict[str, Any]) -> str:
    if not isinstance(entry, dict):
        return str(entry)
    return (
        entry.get("memory")
        or entry.get("content")
        or entry.get("text")
        or entry.get("data")
        or str(entry)
    )


def _safe_delete_all(memory, *, user_id: Optional[str] = None) -> None:
    try:
        memory.delete_all(user_id=user_id)
    except Exception:
        pass


def test_step1_setup() -> None:
    _print_step("Step 1: Setup")
    memory = create_memory()
    print(memory.config)
    print("✓ Memory initialized successfully!")


def test_step2_add_first_memory() -> None:
    _print_step("Step 2: Add Your First Memory")
    memory = create_memory()
    user_id = "user123"
    _safe_delete_all(memory, user_id=user_id)

    result = memory.add(messages="User likes Python programming", user_id=user_id)
    memory_id = _extract_memory_id(result) or "N/A"
    print(f"✓ Memory added! ID: {memory_id}")
    _safe_delete_all(memory, user_id=user_id)


def test_step3_add_multiple_memories() -> None:
    _print_step("Step 3: Add Multiple Memories")
    memory = create_memory()
    user_id = "user123_multi"
    _safe_delete_all(memory, user_id=user_id)

    memories = [
        "User likes Python programming",
        "User prefers email support over phone calls",
        "User works as a software engineer",
        "User favorite color is blue",
    ]

    for mem in memories:
        memory.add(messages=mem, user_id=user_id)
        print(f"✓ Added: {mem}")

    print(f"\n✓ All memories added for user {user_id}")
    _safe_delete_all(memory, user_id=user_id)


def test_step4_search_memories() -> None:
    _print_step("Step 4: Search Memories")
    memory = create_memory()
    user_id = "user123_search"
    _safe_delete_all(memory, user_id=user_id)

    memory.add("User likes Python programming", user_id=user_id)
    memory.add("User prefers email support", user_id=user_id)
    memory.add("User works as a software engineer", user_id=user_id)

    print("Searching for 'user preferences'...")
    results = memory.search(query="user preferences", user_id=user_id, limit=5)
    results_list = list(_get_results_list(results))
    print(f"\nFound {len(results_list)} memories:")
    for index, entry in enumerate(results_list, start=1):
        print(f"  {index}. {_memory_text(entry)}")
    _safe_delete_all(memory, user_id=user_id)


def test_step5_add_with_metadata() -> None:
    _print_step("Step 5: Add Metadata")
    memory = create_memory()
    user_id = "user123_metadata"
    _safe_delete_all(memory, user_id=user_id)

    memory.add(
        messages="User likes Python programming",
        user_id=user_id,
        metadata={
            "category": "preference",
            "importance": "high",
            "source": "conversation",
        },
    )

    memory.add(
        messages="User prefers email support",
        user_id=user_id,
        metadata={
            "category": "communication",
            "importance": "medium",
        },
    )

    print("✓ Memories added with metadata")
    _safe_delete_all(memory, user_id=user_id)


def test_step6_search_with_metadata_filters() -> None:
    _print_step("Step 6: Search with Metadata Filters")
    memory = create_memory()
    user_id = "user123_metadata_filter"
    _safe_delete_all(memory, user_id=user_id)

    memory.add(
        messages="User likes Python programming",
        user_id=user_id,
        metadata={"category": "preference"},
    )
    memory.add(
        messages="User prefers email support",
        user_id=user_id,
        metadata={"category": "communication"},
    )

    print("Searching with metadata filter...")
    results = memory.search(
        query="user preferences",
        user_id=user_id,
        filters={"category": "preference"},
    )

    filtered_results = list(_get_results_list(results))
    print(f"\nFound {len(filtered_results)} memories:")
    for entry in filtered_results:
        print(f"  - {_memory_text(entry)}")
        metadata = entry.get("metadata") if isinstance(entry, dict) else None
        print(f"    Metadata: {metadata or {}}")

    _safe_delete_all(memory, user_id=user_id)


def test_step7_get_all_memories() -> None:
    _print_step("Step 7: Get All Memories")
    memory = create_memory()
    user_id = "user123_all"
    _safe_delete_all(memory, user_id=user_id)

    memory.add("User likes Python", user_id=user_id)
    memory.add("User prefers email", user_id=user_id)
    memory.add("User works as engineer", user_id=user_id)

    all_memories = memory.get_all(user_id=user_id)
    results_list = list(_get_results_list(all_memories))

    print(f"\nTotal memories for {user_id}: {len(results_list)}")
    print("\nAll memories:")
    for index, entry in enumerate(results_list, start=1):
        print(f"  {index}. {_memory_text(entry)}")

    _safe_delete_all(memory, user_id=user_id)


def test_step8_update_memory() -> None:
    _print_step("Step 8: Update a Memory")
    memory = create_memory()
    user_id = "user123_update"
    _safe_delete_all(memory, user_id=user_id)

    original_content = "User likes Python programming"
    result = memory.add(messages=original_content, user_id=user_id, infer=False)
    memory_id = _extract_memory_id(result)
    if memory_id is None:
        raise RuntimeError("Failed to create memory for update step.")

    updated_content = (
        "User loves Python programming, especially for data science"
    )
    memory.update(memory_id=memory_id, content=updated_content, user_id=user_id)

    updated_memory = memory.get(memory_id=memory_id, user_id=user_id) or {}
    new_text = _memory_text(updated_memory)

    print("✓ Memory updated!")
    print(f"  Old: {original_content}")
    print(f"  New: {new_text}")

    _safe_delete_all(memory, user_id=user_id)


def test_step9_delete_memory() -> None:
    _print_step("Step 9: Delete a Memory")
    memory = create_memory()
    user_id = "user123_delete"
    _safe_delete_all(memory, user_id=user_id)

    result = memory.add(
        messages="User likes Python programming", user_id=user_id, infer=False
    )
    memory_id = _extract_memory_id(result)
    if memory_id is None:
        raise RuntimeError("Failed to create memory for delete step.")

    success = memory.delete(memory_id=memory_id, user_id=user_id)
    if success:
        print(f"✓ Memory {memory_id} deleted successfully!")
    else:
        print("✗ Failed to delete memory")

    _safe_delete_all(memory, user_id=user_id)


def test_step10_delete_all_memories() -> None:
    _print_step("Step 10: Delete All Memories")
    memory = create_memory()
    user_id = "user123_delete_all"
    _safe_delete_all(memory, user_id=user_id)

    memory.add("Alice is 1 years old", user_id=user_id)
    memory.add("Bob is 2 years old", user_id=user_id)
    memory.add("Charlie is 3 years old", user_id=user_id)

    all_memories = memory.get_all(user_id=user_id)
    count_before = len(list(_get_results_list(all_memories)))

    success = memory.delete_all(user_id=user_id)
    if success:
        print(f"✓ Deleted {count_before} memories for {user_id}")
    else:
        print("✗ Failed to delete memories")

    _safe_delete_all(memory, user_id=user_id)


def test_full_example() -> None:
    _print_step("Complete Example")
    memory = create_memory()
    user_id = "demo_user"
    _safe_delete_all(memory, user_id=user_id)

    print("1. Adding memories...")
    memories = [
        "User likes Python programming",
        "User prefers email support",
        "User works as a software engineer",
        "User favorite color is blue",
    ]
    for mem in memories:
        memory.add(messages=mem, user_id=user_id, metadata={"source": "demo"})
        print(f"   ✓ Added: {mem}")

    print("\n2. Searching memories...")
    results = memory.search(query="user preferences", user_id=user_id, limit=5)
    results_list = list(_get_results_list(results))
    print(f"   Found {len(results_list)} memories:")
    for entry in results_list:
        print(f"     - {_memory_text(entry)}")

    print("\n3. Getting all memories...")
    all_memories = memory.get_all(user_id=user_id)
    all_results = list(_get_results_list(all_memories))
    print(f"   Total: {len(all_results)} memories")

    print("\n4. Cleaning up...")
    count_before = len(all_results)
    delete_success = memory.delete_all(user_id=user_id)
    if delete_success:
        print(f"   ✓ Deleted {count_before} memories")
    else:
        print("   ✗ Failed to delete memories")

    _safe_delete_all(memory, user_id=user_id)


def test_extension_exercise() -> None:
    _print_step("Extension Exercise: Multiple Users and Metadata Search")
    memory = create_memory()
    _safe_delete_all(memory, user_id="user1")
    _safe_delete_all(memory, user_id="user2")
    _safe_delete_all(memory, user_id="user123")

    memory.add("User 1 likes Python", user_id="user1")
    memory.add("User 2 likes Java", user_id="user2")

    results_user1 = memory.search("preferences", user_id="user1")
    results_user2 = memory.search("preferences", user_id="user2")

    print("Results for user1:")
    for entry in _get_results_list(results_user1):
        print(f"  - {_memory_text(entry)}")

    print("\nResults for user2:")
    for entry in _get_results_list(results_user2):
        print(f"  - {_memory_text(entry)}")

    memory.add(
        messages="User preference",
        user_id="user123",
        metadata={
            "category": "preference",
            "importance": "high",
            "source": "conversation",
            "timestamp": "2024-01-01",
            "tags": ["python", "programming"],
        },
    )

    print("\nSearch by category for user123:")
    category_results = memory.search(
        query="programming languages",
        user_id="user123",
    )
    for entry in _get_results_list(category_results):
        print(f"  - {_memory_text(entry)}")
        metadata = entry.get("metadata") if isinstance(entry, dict) else None
        print(f"    Metadata: {metadata or {}}")

    print("\nSearch with different limit for user123:")
    limit_results = memory.search(
        query="user information",
        user_id="user123",
        limit=10,
    )
    for entry in _get_results_list(limit_results):
        print(f"  - {_memory_text(entry)}")
        metadata = entry.get("metadata") if isinstance(entry, dict) else None
        if metadata:
            print(f"    Metadata: {metadata}")

    _safe_delete_all(memory, user_id="user1")
    _safe_delete_all(memory, user_id="user2")
    _safe_delete_all(memory, user_id="user123")

def test_main() -> None:
    
    _print_banner("Powermem Scenario 1: Basic Usage")
    # Core scenario steps
    test_step1_setup()
    test_step2_add_first_memory()
    test_step3_add_multiple_memories()
    test_step4_search_memories()
    test_step5_add_with_metadata()
    test_step6_search_with_metadata_filters()
    test_step7_get_all_memories()
    test_step8_update_memory()
    test_step9_delete_memory()
    test_step10_delete_all_memories()

    test_full_example()
    test_extension_exercise()

    _print_banner("Scenario 1 walkthrough completed successfully!")


if __name__ == "__main__":
    test_main()

