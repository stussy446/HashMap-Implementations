# Name: Steve Rector
# OSU Email: rectors@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 HashMap
# Due Date: 12/2/2022
# Description: Implements a Hashmap using Open Addressing with Quadratic Probing

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If given key already exists, its associated
        value is replaced with the new value. If given key is not in hash map, new key/value
        pair is formed

        :param key: key to be modified or inserted into the hash map
        :type key: str
        :param value: object to be set as the value of the provided key
        :type value: object
        """
        # if the load factor is greater than or equal to 0.5, resize the table
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        hash_value = self._hash_function(key) % self._capacity
        hash_entry = HashEntry(key, value)
        j = 1
        # if key is already in the hashmap, replace its value and return
        if self.contains_key(key):
            while self._buckets[hash_value].key != key:
                hash_value = (self._hash_function(key) + j ** 2) % self.get_capacity()
                j += 1

            self._buckets[hash_value].value = value
            return

        # traverses using quadratic probing until a tombstone spot is found that can be inserted into or an empty
        # spot is found
        while self._buckets[hash_value] is not None:
            if self._buckets[hash_value].is_tombstone:
                self._buckets[hash_value] = hash_entry
                self._size += 1
                return

            hash_value = (self._hash_function(key) + j**2) % self.get_capacity()
            j += 1

        self._buckets[hash_value] = hash_entry
        self._size += 1

    def table_load(self) -> float:
        """
        Returns the current hash table load factor

        :return: float representing tables current load factor
        :rtype: float
        """
        return self.get_size() / self.get_capacity()

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table

        :return: integer representing number of empty buckets in the hash table
        :rtype: int
        """
        return self.get_capacity() - self.get_size()


    def resize_table(self, new_capacity: int) -> None:
        """
        Changes capacity of the internal hash table, with all existing key/value pairs remaining in the new hash map
        with newly rehashed table links

        :param new_capacity: new capacity to set the hash table to
        :type new_capacity: int
        """
        # return if the new capacity is less than the current capacity
        if new_capacity < self.get_size():
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        new_buckets = DynamicArray()
        old_buckets = self._buckets

        for i in range(0, new_capacity):
            new_buckets.append(None)

        self._buckets = new_buckets
        self._size = 0
        self._capacity = new_capacity

        for i in range(0, old_buckets.length()):
            if old_buckets[i] is not None:
                hash_entry = old_buckets[i]
                self.put(hash_entry.key, hash_entry.value)

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. If the key is not in the hash map then method returns None

        :param key: key to be searched for in the hashmap
        :type key: str
        :return: Object stored at the key vlue pair in the hashmap, or None if key is not there
        :rtype: object
        """
        if not self.contains_key(key):
            return None

        current_hash_value = self._hash_function(key) % self.get_capacity()
        current_hash_entry = self._buckets[current_hash_value]
        j = 1

        while current_hash_entry is not None:
            if current_hash_entry.key == key:
                if current_hash_entry.is_tombstone:
                    return None
                else:
                    return current_hash_entry.value

            current_hash_value = (self._hash_function(key) + j**2) % self.get_capacity()
            current_hash_entry = self._buckets[current_hash_value]
            j += 1

        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise returns False

        :param key: key to search for in the hashmap
        :type key: str
        :return: True if key is in hash map, False otherwise
        :rtype: bool
        """
        if self.get_size() == 0:
            return False

        current_hash_value = self._hash_function(key) % self.get_capacity()
        current_hash_entry = self._buckets[current_hash_value]
        j = 1

        # continue traversing the array with quadratic probing until key is found or a non tombstone empty
        # index is found
        while current_hash_entry is not None:
            # if the key is found but a tombstone, return False since it is not really in the map if it is a tombstone
            if current_hash_entry.key == key:
                if current_hash_entry.is_tombstone:
                    return False
                else:
                    return True

            current_hash_value = (self._hash_function(key) + j**2) % self.get_capacity()
            current_hash_entry = self._buckets[current_hash_value]
            j += 1

        # returns false if going past the while loop, as that indicates the key is non-existant
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and value from the hash map. If key is not in hash map, returns
        :param key: Key from key value pair to be removed from hash map
        :type key: str
        """
        if not self.contains_key(key):
            return

        hash_value = self._hash_function(key) % self.get_capacity()
        hash_entry = self._buckets[hash_value]
        j = 1
        while hash_entry.key != key:
            hash_value = (self._hash_function(key) + j**2) % self.get_capacity()
            hash_entry = self._buckets[hash_value]
            j += 1

        hash_entry.is_tombstone = True
        self._size -= 1

    def clear(self) -> None:
        """
        Clears the contents of the hash map without changing the underlying hash table capacity
        """
        for i in range(0, self._capacity):
            self._buckets[i] = None

        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DynamicArray where each index contains a tuple of a key/vlue pair stored in the Hash Map.

        :return: DynamicArray containing tuples of each key/value pair
        :rtype: DynamicArray
        """
        new_da = DynamicArray()

        for i in range(0, self.get_capacity()):
            if self._buckets[i] is not None:
                if not self._buckets[i].is_tombstone:
                    hash_entry = self._buckets[i]
                    new_tuple = (hash_entry.key, hash_entry.value)
                    new_da.append(new_tuple)

        return new_da

    def __iter__(self):
        """Creates the iterator for loop"""
        self._index = 0

        return self

    def __next__(self) -> HashEntry:
        """Obtain the next HashEntry and advance the iterator"""
        value = self._buckets[self._index]

        while value is None:
            if self._index >= self.get_capacity() - 1:
                raise StopIteration
            self._index += 1
            value = self._buckets[self._index]

        self._index += 1

        return value

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
