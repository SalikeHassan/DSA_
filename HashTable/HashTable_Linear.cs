using System;

public class Entry
{
    public string Key { get; set; }
    public int Value { get; set; }
    public bool IsDeleted { get; set; }

    public Entry(string key, int value)
    {
        Key = key;
        Value = value;
        IsDeleted = false;
    }
}

public class HashTableLinearProbing
{
    private int capacity;
    private Entry[] table;
    private int size;

    public HashTableLinearProbing(int capacity = 10)
    {
        this.capacity = capacity;
        this.table = new Entry[capacity];
        this.size = 0;
    }

    private int HashFunction(string key)
    {
        return Math.Abs(key.GetHashCode()) % capacity;
    }

    public void Put(string key, int value)
    {
        if (size >= capacity)
        {
            Console.WriteLine("Hash table is full!");
            return;
        }

        int index = HashFunction(key);
        int originalIndex = index;
        int probeCount = 0;

        // Linear probe until we find empty slot or matching key
        while (table[index] != null && !table[index].IsDeleted)
        {
            if (table[index].Key == key)
            {
                // Key exists, update value
                table[index].Value = value;
                Console.WriteLine($"Updated '{key}' at index {index}");
                return;
            }

            // Move to next slot (with wraparound)
            probeCount++;
            index = (index + 1) % capacity;

            // Prevent infinite loop
            if (index == originalIndex)
            {
                Console.WriteLine("Table is full, cannot insert!");
                return;
            }
        }

        // Found empty slot or deleted entry
        table[index] = new Entry(key, value);
        size++;
        Console.WriteLine($"Stored '{key}' at index {index} (probed {probeCount} times)");
    }

    public int Get(string key)
    {
        int index = HashFunction(key);
        int originalIndex = index;

        // Linear probe until we find the key
        while (table[index] != null)
        {
            if (!table[index].IsDeleted && table[index].Key == key)
            {
                return table[index].Value;
            }

            index = (index + 1) % capacity;

            // We've checked all slots
            if (index == originalIndex)
            {
                break;
            }
        }

        throw new KeyNotFoundException($"Key '{key}' not found");
    }

    public bool Remove(string key)
    {
        int index = HashFunction(key);
        int originalIndex = index;

        while (table[index] != null)
        {
            if (!table[index].IsDeleted && table[index].Key == key)
            {
                table[index].IsDeleted = true;
                size--;
                Console.WriteLine($"Removed '{key}' from index {index}");
                return true;
            }

            index = (index + 1) % capacity;

            if (index == originalIndex)
            {
                break;
            }
        }

        return false;
    }

    public void Display()
    {
        for (int i = 0; i < capacity; i++)
        {
            if (table[i] == null)
            {
                Console.WriteLine($"Index {i}: [empty]");
            }
            else if (table[i].IsDeleted)
            {
                Console.WriteLine($"Index {i}: [deleted]");
            }
            else
            {
                Console.WriteLine($"Index {i}: {table[i].Key} -> {table[i].Value}");
            }
        }
        Console.WriteLine($"Total items: {size}\n");
    }
}

public class Program
{
    public static void Main()
    {
        HashTableLinearProbing hashTable = new HashTableLinearProbing(7);

        string[] keys = { "apple", "banana", "orange", "grape", "melon" };
        int[] values = { 10, 20, 30, 40, 50 };

        Console.WriteLine("1. Inserting items:");
        for (int i = 0; i < keys.Length; i++)
        {
            hashTable.Put(keys[i], values[i]);
        }

        hashTable.Display();

        // Test get operation
        Console.WriteLine("2. Getting values:");
        Console.WriteLine($"apple = {hashTable.Get("apple")}");
        Console.WriteLine($"banana = {hashTable.Get("banana")}");

        // Test remove operation
        Console.WriteLine("\n3. Removing 'orange':");
        hashTable.Remove("orange");
        hashTable.Display();

        // Test collision handling
        Console.WriteLine("4. Adding more items to see collision handling:");
        hashTable.Put("peach", 60);
        hashTable.Put("plum", 70);
        hashTable.Display();

        // Test error handling
        Console.WriteLine("5. Testing error handling:");
        try
        {
            int value = hashTable.Get("cherry"); // This key doesn't exist
        }
        catch (KeyNotFoundException e)
        {
            Console.WriteLine($"Error caught: {e.Message}");
        }
    }
}