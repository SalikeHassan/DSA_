from typing import Any, List, Optional


class Entry:
    
    def __init__(self,key:str,value:Any) -> None:
        self.key:str = key
        self.value:Any = value
        self.is_deleted:bool = False

class HashTableLinearProbing:
    
    def __init__(self, capacity:int=10) -> None:
        self.capacity:int = capacity
        self.table: List[Optional[Entry]] = [None]*self.capacity
        self.size:int = 0
        
    def hash_function(self,key:str) -> int:
        return hash(key) % self.capacity
    
    def put(self, key: Any, value: Any) -> None:
        """Insert or update key-value pair"""
        if self.size >= self.capacity:
            print("Hash table is full!")
            return
        
        index: int = self.hash_function(key)
        original_index: int = index
        probe_count: int = 0
        
        # Linear probe until we find empty slot or matching key
        while self.table[index] is not None and not self.table[index].is_deleted:
            if self.table[index].key == key:
                # Key exists, update value
                self.table[index].value = value
                print(f"Updated '{key}' at index {index}")
                return
            
            # Move to next slot (with wraparound)
            probe_count += 1
            index = (index + 1) % self.capacity
            
            # Prevent infinite loop
            if index == original_index:
                print("Table is full, cannot insert!")
                return
        
        # Found empty slot or deleted entry
        self.table[index] = Entry(key, value)
        self.size += 1
        print(f"Stored '{key}' at index {index} (probed {probe_count} times)")
        
    def get(self, key: Any) -> Any:
        """Retrieve value by key"""
        index: int = self.hash_function(key)
        original_index: int = index
        
        # Linear probe until we find the key
        while self.table[index] is not None:
            if not self.table[index].is_deleted and self.table[index].key == key:
                return self.table[index].value
            
            index = (index + 1) % self.capacity
            
            # We've checked all slots
            if index == original_index:
                break
        
        raise KeyError(f"Key '{key}' not found")
    
    def remove(self,key:Any) -> bool:
        index:int = self.hash_function(key)
        
        original_index:int = index
        
        while self.table[index] is not None:
            if not self.table[index].is_deleted and self.table[index].key == key:
                self.table[index].is_deleted = True
                self.size -= 1
                print(f"Removed '{key}' from index {index}")
                return True
            
            index = (index + 1) % self.capacity
            
            if  index == original_index:
                break
        
        return False
    
    def display(self) -> None:
        
        for i in range(self.capacity):
            if self.table[i] is None:
                print(f"Index {i}: [empty]")
            elif self.table[i].is_deleted:
                print(f"Index {i} [deleted]")
            else:
                print(f"Index {i}: {self.table[i].key} -> {self.table[i].value}")
                
        print(f"Total items: {self.size}\n")

def main()->None:
    hash_table = HashTableLinearProbing(7)
    
    items = [
        ("apple", 10),
        ("banana", 20),
        ("orange", 30),
        ("grape", 40),
        ("melon", 50)
    ]
    
    for key, value in items:
        hash_table.put(key,value)
        
    hash_table.display()
    
    # Test get operation
    print("2. Getting values:")
    print(f"apple = {hash_table.get('apple')}")
    print(f"banana = {hash_table.get('banana')}")
    
    # Test remove operation
    print("\n3. Removing 'orange':")
    hash_table.remove("orange")
    hash_table.display()
    
    # Test collision handling
    print("4. Adding more items to see collision handling:")
    hash_table.put("peach", 60)
    hash_table.put("plum", 70)
    hash_table.display()
    
    # Test error handling
    print("5. Testing error handling:")
    try:
        value = hash_table.get("cherry")  # This key doesn't exist
    except KeyError as e:
        print(f"Error caught: {e}")


if __name__ == "__main__":
    main()

                

                
            