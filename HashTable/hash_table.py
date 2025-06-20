class KeyValuePair:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class SimpleHashTable:
    def __init__(self, size=10):
        self.capacity = size
        self.table = [None] * self.capacity
    
    def hash_function(self,key):
        if key is None:
            raise ValueError("Key can not be null")
        
        hash_code = abs(hash(key))
        
        return hash_code % self.capacity
    
    def put(self, key,value):
        index = self.hash_function(key)
        
        pair = KeyValuePair(key,value)
        
        self.table[index] = pair
        
        print(f"Stored '{key}' -> '{value}' at index '{index}'")
        
    def get(self,key):
        index = self.hash_function(key)
        
        if  self.table[index] is None:
            raise KeyError(f"Key '{key}' not found")
        
        return self.table[index].value
    
    def contains(self,key):
        index = self.hash_function(key)
        
        return (self.table[index] is not None and self.table[index].key == key)
    
    def display(self):
        for i in range(self.capacity):
            if self.table[i] is not None:
                print(f"Index '{i}' : {self.table[i].key} -> {self.table[i].value}")
            

if __name__ == "__main__":
    
    hash_table = SimpleHashTable(5)
    
    print("Adding items:")
    
    hash_table.put("apple",10)
    hash_table.put("orange",20)
    hash_table.put("banana",30)
    
    hash_table.display()