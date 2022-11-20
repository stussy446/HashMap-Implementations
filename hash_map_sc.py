# Name: Steve Rector
# OSU Email: rectors@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 HashMap
# Due Date: 12/2/2022
# Description: Implements a Hashmap using Separate Chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        # if the load factor is greater than or equal to 1, resize the table
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        hash_value = self._hash_function(key) % self._capacity
        ll = self._buckets[hash_value]

        # if the linked list at the index contains the key, set the nodes value to the new value and return
        found_node = ll.contains(key)
        if found_node is not None:
            found_node.value = value
            return

        ll.insert(key, value)
        self._size += 1


    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table

        :return: Number of empty bucks in hash table
        :rtype: int
        """
        empty_count = 0

        for i in range(0, self.get_capacity()):
            if self._buckets[i].length() == 0:
                empty_count += 1

        return empty_count

    def table_load(self) -> float:
        """
        Returns the current hash table load factor

        :return: current load factor of the hash table
        :rtype: float
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears the contents of the hash map without changing underlying capacity
        """

        for i in range(0, self._capacity):
            self._buckets[i] = LinkedList()

        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table, with all existing pairs remaining in the new hash map with
        newly rehashed table links

        :param new_capacity: new capacity to set the hash table to
        :type new_capacity: int
        """
        if new_capacity < 1:
            return

        # set the new_capacity to the next available prime number as needed
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)
        self._capacity = new_capacity

        # sets up a new DynamicArray with the amount of buckets equal to the new capacity
        new_buckets = DynamicArray()
        count = 0
        while count < self.get_capacity():
            new_buckets.append(LinkedList())
            count += 1

        # Moves each node to their new spot on the map based off of the nodes new hash value
        old_da = self._buckets
        self._buckets = new_buckets
        self._size = 0
        for i in range(0, old_da.length()):
            for node in old_da[i]:
                self.put(node.key, node.value)

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. If the key is not in the hash map,
        returns None

        :param key: key whose value we are getting
        :type key: str
        :return: value object associated with the key
        :rtype: object
        """
        hash_value = self._hash_function(key) % self.get_capacity()

        for node in self._buckets[hash_value]:
            if node.key == key:
                return node.value

        return None

    def contains_key(self, key: str) -> bool:
        """
        Return True if the given key is in the hash map, otherwise returns False

        :param key: key to search for in the hash map
        :type key: str
        :return: True if key is in the hash map, False otherwise
        :rtype: bool
        """
        hash_value = self._hash_function(key) % self.get_capacity()
        node = self._buckets[hash_value].contains(key)

        if node is not None:
            return True

        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key value pair from the hash map. If the key is not in the hash map, the method does nothing

        :param key: key to be searched for in the hash map
        :type key: str
        """
        hash_value = self._hash_function(key) % self.get_capacity()

        removed_node = self._buckets[hash_value].remove(key)

        if removed_node:
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DynamicArray where each index contains a tuple of a key/value pair from the hashmap

        :return: DynamicArray containing tuples of each key/value pair in the hashmap
        :rtype: DynamicArray
        """
        new_da = DynamicArray()

        for i in range(0, self._buckets.length()):
            for node in self._buckets[i]:
                new_tuple = (node.key, node.value)
                new_da.append(new_tuple)

        return new_da


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Receives a DynamicArray and returns a tuple containing (in order) a DynamicArray comprising the mode value(s) of the
    array and an integer representing the highest frequency (how many times they appear)

    :param da: DynamicArray in which the mode/frequenc will be determined
    :return: tuple containing a DynamicArray of all the highest frequency keys, and the frequency they occur
    :rtype: tuple
    """
    map = HashMap()
    highest_frequency = 1

    # places all elements of array into the map, if it is the first time seeing the key set its value to 1, otherwise
    # add one to its value each time
    for i in range(0, da.length()):
        current_key = da[i]

        if not map.contains_key(current_key):
            map.put(current_key, 1)
        else:
            new_value = map.get(current_key) + 1
            map.put(current_key, new_value)

            # changes the highest frequency if the keys value is now greater than previous highest frequency
            if new_value > highest_frequency:
                highest_frequency = new_value

    mode_da = DynamicArray()
    pairs = map.get_keys_and_values()
    
    # puts all the highest frequency keys into the mode_da DynamicArray
    for i in range(0, pairs.length()):
        current_key = pairs[i][0]
        value = pairs[i][1]
        if value == highest_frequency:
            mode_da.append(current_key)

    return mode_da, highest_frequency


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

    print("steve resize test")
    print("----------------------")
    m = HashMap(3, hash_function_1)
    m.put('a', 10)
    print(m.get_size(), m.get_capacity(), m.get('a'), m.contains_key('a'))
    m.resize_table(7)
    print(m.get_size(), m.get_capacity(), m.get('a'), m.contains_key('a'))

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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
