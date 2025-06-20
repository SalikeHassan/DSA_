from typing import Optional, List, Any, Union

class Node:
    """A node in the hash table's linked list for collision handling."""
    
    def __init__(self, key: str, value: Any) -> None:
        self.key: str = key
        self.value: Any = value
        self.next: Optional['Node'] = None

class HashTableChaining:
    """Hash table implementation using chaining for collision resolution."""
    
    def __init__(self, capacity: int = 10) -> None:
        self.capacity: int = capacity
        self.buckets: List[Optional[Node]] = [None] * capacity
        self.size: int = 0
    
    def get_hash_value(self, key: str) -> int:
        """Calculate hash value for a given key."""
        hash_value: int = hash(key)
        return hash_value % self.capacity
    
    def put(self, key: str, value: Any) -> None:
        """Insert or update a key-value pair in the hash table."""
        index: int = self.get_hash_value(key)
        new_node: Node = Node(key, value)  # Fixed: was None(key, value)
        
        if self.buckets[index] is None:
            self.buckets[index] = new_node
            self.size += 1
            print(f"Stored '{key}' at index {index}")
        else:
            current: Optional[Node] = self.buckets[index]
            previous: Optional[Node] = None
            
            while current:
                if current.key == key:
                    current.value = value
                    print(f"Updated '{key}' at index {index}")
                    return
                previous = current
                current = current.next
            
            # Add to end of chain
            if previous:
                previous.next = new_node
            self.size += 1
            print(f"Stored '{key}' at index {index} (added to chain)")
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve value for a given key."""
        index: int = self.get_hash_value(key)
        current: Optional[Node] = self.buckets[index]
        
        while current:
            if current.key == key:
                return current.value  # Fixed: was missing current.value
            current = current.next
        
        return None  # Key not found
    
    def remove(self, key: str) -> bool:
        """Remove a key-value pair from the hash table."""
        index: int = self.get_hash_value(key)
        current: Optional[Node] = self.buckets[index]
        previous: Optional[Node] = None
        
        while current:
            if current.key == key:
                if previous is None:
                    # Removing first node in chain
                    self.buckets[index] = current.next
                else:
                    # Removing node from middle/end of chain
                    previous.next = current.next
                self.size -= 1
                print(f"Removed '{key}' from index {index}")
                return True
            previous = current
            current = current.next
        
        print(f"Key '{key}' not found")
        return False
    
    def display(self) -> None:
        """Display the current state of the hash table."""
        print("\nHash Table Contents:")
        print("-" * 20)
        for i in range(self.capacity):
            print(f"Bucket {i}: ", end="")
            current: Optional[Node] = self.buckets[i]
            
            if current is None:
                print("Empty")
            else:
                chain_items: List[str] = []
                while current:
                    chain_items.append(f"({current.key}: {current.value})")
                    current = current.next
                print(" -> ".join(chain_items))
        print(f"\nTotal items: {self.size}")
        print(f"Load factor: {self.size / self.capacity:.2f}")

def main() -> None:
    """Demonstrate hash table collision handling."""
    print("HASH TABLE COLLISION HANDLING DEMONSTRATION")
    print("==========================================\n")
    
    # Create hash table with small capacity to force collisions
    hash_table: HashTableChaining = HashTableChaining(capacity=5)
    
    # Test data that will cause collisions
    test_data: List[tuple[str, int]] = [
        ("apple", 10),
        ("banana", 20),
        ("grape", 30),
        ("orange", 40),
        ("melon", 50),
        ("peach", 60)
    ]
    
    # Insert all items
    print("Inserting items:")
    for key, value in test_data:
        hash_table.put(key, value)
    
    # Display hash table state
    hash_table.display()
    
    # Test retrieval
    print("\nTesting retrieval:")
    for key, expected_value in test_data:
        retrieved_value: Optional[Any] = hash_table.get(key)
        print(f"get('{key}'): {retrieved_value} {'✓' if retrieved_value == expected_value else '✗'}")
    
    # Test updating existing key
    print("\nUpdating existing key:")
    hash_table.put("apple", 100)
    print(f"get('apple'): {hash_table.get('apple')}")
    
    # Test removal
    print("\nTesting removal:")
    hash_table.remove("banana")
    hash_table.remove("nonexistent")
    
    # Final state
    hash_table.display()

if __name__ == "__main__":
    main()