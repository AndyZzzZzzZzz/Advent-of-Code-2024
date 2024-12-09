def parse_disk_map(disk_map):
    blocks = []
    file_id = 0
    is_file_length = True  # Start with file length

    for idx, char in enumerate(disk_map):
        length = int(char)
        if is_file_length:
            # Append the file ID `length` times
            blocks.extend([file_id] * length)
            file_id += 1
        else:
            # Append free space `length` times
            blocks.extend(['.'] * length)
        is_file_length = not is_file_length  # Toggle between file and free space

    return blocks

def compact_disk(blocks):
    # Convert the list to allow modifications
    word_list = blocks.copy()
    pos0 = 0
    pos1 = len(word_list) - 1

    while pos0 < pos1:
        # Move pos0 to the next free space
        while pos0 < pos1 and word_list[pos0] != '.':
            pos0 += 1
        # Move pos1 to the previous non-free space
        while pos0 < pos1 and word_list[pos1] == '.':
            pos1 -= 1

        
        if pos0 < pos1:
            # Replace the dot at pos0 with the character at pos1
            word_list[pos0] = word_list[pos1]
            # Replace the character at pos1 with a dot to prevent reuse
            word_list[pos1] = '.'
            # Move both pointers inward
            pos0 += 1
            pos1 -= 1

        

    return word_list

def compact_disk2(blocks):
    # Create a copy of the blocks to modify
    word_list = blocks.copy()
    pos1 = len(word_list) - 1

    # Move pos1 to the last non-free block
    while pos1 >= 0 and word_list[pos1] == '.':
        pos1 -= 1

    while pos1 >= 0:
        letter = word_list[pos1]
        letter_space = 0
        temp1 = pos1

        # Count the number of consecutive blocks for the current file
        while temp1 >= 0 and word_list[temp1] == letter:
            letter_space += 1
            temp1 -= 1

        # Find the first suitable space from the left to place the blocks
        pos0 = 0
        while pos0 < pos1:
            if word_list[pos0] != '.':
                pos0 += 1
                continue

            # Check if there's enough space to place the blocks
            space_available = 0
            temp = pos0
            while temp < len(word_list) and word_list[temp] == '.':
                space_available += 1
                temp += 1

            if space_available >= letter_space:
                # Move the blocks to the left
                for i in range(letter_space):
                    word_list[pos0 + i] = letter
                    word_list[pos1 - i] = '.'
                break  # Move to the next set of blocks

            pos0 = temp  # Move to the next potential space

        # Update pos1 to the next set of blocks
        pos1 = temp1

    return word_list


def calculate_checksum(blocks):
    checksum = 0
    for position, block in enumerate(blocks):
        if block != '.':
            checksum += position * block
    return checksum

def main():
    # Read the disk map from the file
    with open('day9/example.txt', 'r') as file:
        data = file.read().strip()

    # Parse the disk map into blocks
    blocks = parse_disk_map(data)
    #print("Initial Blocks:")
    #print(blocks)  # Display as list for clarity

    # Compact the disk by moving file blocks to the left
    compacted_blocks = compact_disk2(blocks)
    #print("\nCompacted Blocks:")
    #print(compacted_blocks)  # Display as list for clarity

    # Calculate the filesystem checksum
    checksum = calculate_checksum(compacted_blocks)
    print(f"\nFilesystem Checksum: {checksum}")

if __name__ == "__main__":
    main()
