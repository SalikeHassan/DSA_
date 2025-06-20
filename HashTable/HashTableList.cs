using System;
using System.Collections.Generic;

public class Node
{
    public string Key { get; set; }
    public int Value { get; set; }
    public Node Next { get; set; }

    public Node(string key, int value)
    {
        Key = key;
        Value = value;
        Next = null;
    }
}

public class HashTableChaining
{
    private int capacity;
    private Node[] buckets;
    private int size;

    public HashTableChaining(int capacity = 10)
    {
        this.capacity = capacity;
        this.buckets = new Node[capacity];
        this.size = 0;
    }

    private int GetHashValue(string key)
    {
        int hashValue = key.GetHashCode();
        return Math.Abs(hashValue) % capacity;
    }

    public void Put(string key, int value)
    {
        int index = GetHashValue(key);
        Node newNode = new Node(key, value);

        if (buckets[index] == null)
        {
            buckets[index] = newNode;
            size++;
            Console.WriteLine($"Stored '{key}' at index {index}");
        }
        else
        {
            Node current = buckets[index];
            Node previous = null;

            while (current != null)
            {
                if (current.Key == key)
                {
                    current.Value = value;
                    Console.WriteLine($"Updated '{key}' at index {index}");
                    return;
                }
                previous = current;
                current = current.Next;
            }

            // Add to end of chain
            if (previous != null)
            {
                previous.Next = newNode;
            }
            size++;
            Console.WriteLine($"Stored '{key}' at index {index} (added to chain)");
        }
    }

    public int? Get(string key)
    {
        int index = GetHashValue(key);
        Node current = buckets[index];

        while (current != null)
        {
            if (current.Key == key)
            {
                return current.Value;
            }
            current = current.Next;
        }

        return null; // Key not found
    }

    public bool Remove(string key)
    {
        int index = GetHashValue(key);
        Node current = buckets[index];
        Node previous = null;

        while (current != null)
        {
            if (current.Key == key)
            {
                if (previous == null)
                {
                    // Removing first node in chain
                    buckets[index] = current.Next;
                }
                else
                {
                    // Removing node from middle/end of chain
                    previous.Next = current.Next;
                }
                size--;
                Console.WriteLine($"Removed '{key}' from index {index}");
                return true;
            }
            previous = current;
            current = current.Next;
        }

        Console.WriteLine($"Key '{key}' not found");
        return false;
    }

    public void Display()
    {
        Console.WriteLine("\nHash Table Contents:");
        Console.WriteLine("--------------------");
        
        for (int i = 0; i < capacity; i++)
        {
            Console.Write($"Bucket {i}: ");
            Node current = buckets[i];

            if (current == null)
            {
                Console.WriteLine("Empty");
            }
            else
            {
                List<string> chainItems = new List<string>();
                while (current != null)
                {
                    chainItems.Add($"({current.Key}: {current.Value})");
                    current = current.Next;
                }
                Console.WriteLine(string.Join(" -> ", chainItems));
            }
        }
        
        Console.WriteLine($"\nTotal items: {size}");
        Console.WriteLine($"Load factor: {(double)size / capacity:F2}");
    }
}

public class Program
{
    public static void Main()
    {
        Console.WriteLine("HASH TABLE COLLISION HANDLING DEMONSTRATION");
        Console.WriteLine("==========================================\n");

        // Create hash table with small capacity to force collisions
        HashTableChaining hashTable = new HashTableChaining(5);

        // Test data that will cause collisions
        string[] keys = { "apple", "banana", "grape", "orange", "melon", "peach" };
        int[] values = { 10, 20, 30, 40, 50, 60 };

        // Insert all items
        Console.WriteLine("Inserting items:");
        for (int i = 0; i < keys.Length; i++)
        {
            hashTable.Put(keys[i], values[i]);
        }

        // Display hash table state
        hashTable.Display();

        // Test retrieval
        Console.WriteLine("\nTesting retrieval:");
        for (int i = 0; i < keys.Length; i++)
        {
            int? retrievedValue = hashTable.Get(keys[i]);
            string status = retrievedValue == values[i] ? "✓" : "✗";
            Console.WriteLine($"get('{keys[i]}'): {retrievedValue} {status}");
        }

        // Test updating existing key
        Console.WriteLine("\nUpdating existing key:");
        hashTable.Put("apple", 100);
        Console.WriteLine($"get('apple'): {hashTable.Get("apple")}");

        // Test removal
        Console.WriteLine("\nTesting removal:");
        hashTable.Remove("banana");
        hashTable.Remove("nonexistent");

        // Final state
        hashTable.Display();
    }
}