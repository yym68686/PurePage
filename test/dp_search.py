from typing import List, Tuple, Dict, Optional
import pypinyin

Matrix = List[List[int]]
SourceMappingData = Dict[str, any]

def extract_boundary_mapping_with_preset_pinyin(original_string: str) -> SourceMappingData:
    pinyin_list = pypinyin.lazy_pinyin(original_string, style=pypinyin.NORMAL)
    pinyin_string = ''
    boundary = []
    original_indices = []

    current_index = 0
    for i, (char, pinyin) in enumerate(zip(original_string, pinyin_list)):
        if char.isascii():
            pinyin_string += char.lower()
            boundary.append([current_index, current_index])
            original_indices.append(i)
            current_index += 1
        else:
            pinyin_string += pinyin
            boundary.append([current_index, current_index + len(pinyin) - 1])
            original_indices.extend([i] * len(pinyin))
            current_index += len(pinyin)

    return {
        'originalString': original_string,
        'pinyinString': pinyin_string,
        'boundary': boundary,
        'originalLength': len(original_string),
        'originalIndices': original_indices
    }


def search_by_boundary_mapping(data: SourceMappingData, target: str, start_index: int, end_index: int) -> Optional[Matrix]:
    original_string = data['originalString'][start_index:end_index+1]
    pinyin_string = data['pinyinString']
    boundary = data['boundary']
    original_indices = data['originalIndices']

    target = target.lower().replace(' ', '')
    target_pinyin = ''.join(pypinyin.lazy_pinyin(target, style=pypinyin.NORMAL))

    dp = [[0] * (len(target_pinyin) + 1) for _ in range(len(pinyin_string) + 1)]

    for i in range(1, len(pinyin_string) + 1):
        for j in range(1, len(target_pinyin) + 1):
            if pinyin_string[i-1] == target_pinyin[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    if dp[-1][-1] != len(target_pinyin):
        return None

    matches = []
    i, j = len(pinyin_string), len(target_pinyin)
    while i > 0 and j > 0:
        if pinyin_string[i-1] == target_pinyin[j-1]:
            matches.append(i-1)
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    matches = matches[::-1]

    hit_indices = []
    for match in matches:
        orig_index = original_indices[match]
        if start_index <= orig_index <= end_index:
            hit_indices.append([orig_index, orig_index])

    merged_indices = []
    for start, end in hit_indices:
        if merged_indices and merged_indices[-1][1] == start - 1:
            merged_indices[-1][1] = end
        else:
            merged_indices.append([start, end])

    return merged_indices if merged_indices else None

def search_with_indexof(source: str, target: str) -> Optional[Matrix]:
    start_index = source.lower().find(target.lower())
    return [[start_index, start_index + len(target) - 1]] if start_index != -1 else None

def search_sentence_by_boundary_mapping(boundary_mapping: SourceMappingData, sentence: str) -> Optional[Matrix]:
    if not sentence:
        return None

    hit_ranges_by_index_of = search_with_indexof(boundary_mapping['originalString'], sentence)
    if hit_ranges_by_index_of:
        return hit_ranges_by_index_of

    return search_by_boundary_mapping(boundary_mapping, sentence, 0, len(boundary_mapping['originalString']) - 1)

def search_entry(source: str, target: str) -> Optional[Matrix]:
    boundary_mapping = extract_boundary_mapping_with_preset_pinyin(source)
    return search_sentence_by_boundary_mapping(boundary_mapping, target)


# def extract_boundary_mapping_with_preset_pinyin(original_string: str) -> SourceMappingData:
#     # 这个函数在实际使用中需要实现，这里我们使用一个简化版本
#     pinyin_string = ''.join([char if char.isascii() else 'x' for char in original_string])
#     boundary = [[i, i] for i in range(len(original_string))]
#     return {
#         'originalString': original_string,
#         'pinyinString': pinyin_string,
#         'boundary': boundary,
#         'originalLength': len(original_string),
#         'originalIndices': list(range(len(original_string)))
#     }

# def search_by_boundary_mapping(data: SourceMappingData, target: str, start_index: int, end_index: int) -> Optional[Matrix]:
#     original_length = data['originalLength']
#     original_indices = data['originalIndices']
#     pinyin_string = data['pinyinString'][original_indices[start_index]:original_indices[end_index]]
#     boundary = data['boundary'][original_indices[start_index]:original_indices[end_index] + 1]

#     target_length = len(target)
#     pinyin_length = len(pinyin_string)

#     if not data or not target or pinyin_length < target_length or not original_length:
#         return None

#     start_boundary = boundary[0][0]
#     end_boundary = boundary[-1][1]

#     match_positions = [-1] * target_length

#     match_index = 0
#     for i in range(pinyin_length):
#         if match_index < target_length and pinyin_string[i] == target[match_index]:
#             match_positions[match_index] = i
#             match_index += 1

#     if match_index < target_length:
#         return None

#     dp_table = [[0, 0, -1, -1] for _ in range(pinyin_length + 1)]
#     dp_scores = [0] * (pinyin_length + 1)
#     dp_match_path = [[None for _ in range(target_length)] for _ in range(pinyin_length + 1)]

#     for match_index, matched_pinyin_index in enumerate(match_positions):
#         matched_pinyin_index += 1

#         current_dp_table_item = dp_table[matched_pinyin_index - 1]
#         current_score = dp_scores[matched_pinyin_index - 1]

#         dp_scores[matched_pinyin_index - 1] = 0
#         dp_table[matched_pinyin_index - 1] = [0, 0, -1, -1]

#         for i in range(matched_pinyin_index, pinyin_length + 1):
#             prev_score = current_score
#             prev_matched_characters, prev_matched_letters, prev_boundary_start, prev_boundary_end = current_dp_table_item

#             current_dp_table_item = dp_table[i]
#             current_score = dp_scores[i]

#             is_new_word = (i - 1 == boundary[i-1][1] - end_boundary and
#                            prev_boundary_start != boundary[i-1][0] - start_boundary)

#             is_continuation = (prev_matched_characters > 0 and
#                                prev_boundary_end == boundary[i-1][1] - end_boundary and
#                                i > 1 and pinyin_string[i-2] == target[match_index-1])

#             is_equal = i > 0 and pinyin_string[i-1] == target[match_index]

#             if is_equal and (is_new_word or is_continuation) and (match_index == 0 or prev_score > 0):
#                 prev_score += prev_matched_letters * 2 + 1
#                 matched_letters_count = prev_matched_letters + 1

#                 if prev_score >= dp_scores[i-1]:
#                     dp_scores[i] = prev_score
#                     dp_table[i] = [
#                         prev_matched_characters + int(is_new_word),
#                         matched_letters_count,
#                         boundary[i-1][0] - start_boundary,
#                         boundary[i-1][1] - end_boundary
#                     ]

#                     original_string_index = boundary[i-1][0] - start_boundary
#                     new_matched = prev_score > dp_scores[i-1]
#                     dp_match_path[i][match_index] = (
#                         [original_string_index - prev_matched_characters + int(not is_new_word),
#                          original_string_index,
#                          matched_letters_count]
#                         if new_matched else dp_match_path[i-1][match_index]
#                     )
#                     continue

#             dp_scores[i] = dp_scores[i-1]
#             dp_match_path[i][match_index] = dp_match_path[i-1][match_index]
#             gap = boundary[i-1][0] - start_boundary - dp_table[i-1][2]
#             is_same_word = lambda: i < len(boundary) - 1 and boundary[i-1][0] == boundary[i][0]
#             is_within_range = i < pinyin_length - 1
#             dp_table[i] = (dp_table[i-1] if gap == 0 or (is_within_range and gap == 1 and is_same_word())
#                            else [0, 0, -1, -1])

#     if dp_match_path[pinyin_length][target_length - 1] is None:
#         return None

#     hit_indices = []
#     g_index = pinyin_length
#     rest_matched = target_length - 1

#     while rest_matched >= 0:
#         start, end, matched_letters = dp_match_path[g_index][rest_matched]
#         hit_indices.insert(0, [start + start_index, end + start_index])
#         g_index = original_indices[start + start_index] - original_indices[start_index] - 1
#         rest_matched -= matched_letters

#     return hit_indices

# def search_with_indexof(source: str, target: str) -> Optional[Matrix]:
#     start_index = source.find(target.strip())
#     return [[start_index, start_index + len(target) - 1]] if start_index != -1 else None

# def search_sentence_by_boundary_mapping(boundary_mapping: SourceMappingData, sentence: str) -> Optional[Matrix]:
#     if not sentence:
#         return None

#     hit_ranges_by_index_of = search_with_indexof(boundary_mapping['originalString'], sentence)
#     if hit_ranges_by_index_of:
#         return hit_ranges_by_index_of

#     words = sentence.strip().split()
#     hit_ranges = []

#     for word in words:
#         rest_ranges = [[0, boundary_mapping['originalLength'] - 1]]  # Simplified for this example
#         is_hit_by_word = False

#         for start, end in rest_ranges:
#             hit_ranges_by_word = search_by_boundary_mapping(boundary_mapping, word, start, end)
#             if hit_ranges_by_word:
#                 is_hit_by_word = True
#                 hit_ranges.extend(hit_ranges_by_word)
#                 break

#         if not is_hit_by_word:
#             return None

#     return hit_ranges

# def search_entry(source: str, target: str) -> Optional[Matrix]:
#     return (search_with_indexof(source, target) or
#             search_sentence_by_boundary_mapping(extract_boundary_mapping_with_preset_pinyin(source), target))

# import time

# def test_search():
#     test_cases = [
#         ("我爱北京天安北京门", "bei"),
#         ("我爱北京天安门", "天安"),
#         ("我爱北京天安门", "我爱北京天安门"),
#         ("Hello世界", "He"),
#         ("Hello世界", "世界"),
#         ("你好hello世界", "hel"),
#         ("你好hello世界", "你好he"),
#         ("我的家在东北松花江上", "松花江"),
#     ]

#     for source, target in test_cases:
#         result = search_entry(source, target)
#         print(f"Source: {source}")
#         print(f"Target: {target}")
#         print(f"Result: {result}")
#         print()

# def performance_test():
#     long_text = "我爱北京天安门天安门上太阳升伟大领袖毛主席指引我们向前进" * 10000
#     search_target = "天安门上太阳升"

#     start_time = time.time()
#     for _ in range(1000):
#         search_entry(long_text, search_target)
#     end_time = time.time()
#     print(search_entry(long_text, search_target))

#     print(f"Performance test:")
#     print(f"Time taken for 100 searches: {end_time - start_time:.4f} seconds")
#     print(f"Average time per search: {(end_time - start_time) / 100:.4f} seconds")

# if __name__ == "__main__":
#     test_search()
#     performance_test()

# import time

# def test_search():
#     test_cases = [
#         ("我爱北京天安门", "北京"),
#         ("我爱北京天安门", "天安"),
#         ("我爱北京天安门", "我爱北京天安门"),
#         ("Hello世界", "He"),
#         ("Hello世界", "世界"),
#         ("你好hello世界", "hel"),
#         ("你好hello世界", "你好he"),
#         ("我的家在东北松花江上", "松花江"),
#         ("我爱北京天安北京门", "bei"),  # 新增：拼音搜索
#         ("我爱北京天安门", "tian an men"),  # 新增：拼音词组搜索
#         ("你好世界Hello", "shi jie he"),  # 新增：混合中英文拼音搜索
#         ("我是中国人", "zhong guo"),  # 新增：完整拼音搜索
#         ("我是中国人", "zhong1 guo2"),  # 新增：带声调的拼音搜索（应该仍然匹配）
#     ]

#     for source, target in test_cases:
#         result = search_entry(source, target)
#         print(f"Source: {source}")
#         print(f"Target: {target}")
#         print(f"Result: {result}")
#         print()

# def performance_test():
#     long_text = "我爱北京天安门天安门上太阳升伟大领袖毛主席指引我们向前进" * 1000
#     search_target = "天安门上太阳升"

#     start_time = time.time()
#     for _ in range(100):
#         search_entry(long_text, search_target)
#     end_time = time.time()

#     print(f"Performance test:")
#     print(f"Time taken for 100 searches: {end_time - start_time:.4f} seconds")
#     print(f"Average time per search: {(end_time - start_time) / 100:.4f} seconds")

# if __name__ == "__main__":
#     test_search()
#     performance_test()


# Test function
def test_search():
    test_cases = [
        ("我爱北京天安门", "北京"),
        ("我爱北京天安门", "天安"),
        ("我爱北京天安门", "我爱北京天安门"),
        ("Hello世界", "He"),
        ("Hello世界", "世界"),
        ("你好hello世界", "hel"),
        ("你好hello世界", "你好he"),
        ("我的家在东北松花江上", "松花江"),
        ("我爱北京天安北京门", "bei"),  # 拼音搜索
        ("我爱北京天安门", "tian an men"),  # 拼音词组搜索
        ("你好世界Hello", "shi jie he"),  # 混合中英文拼音搜索
        ("我是中国人", "zhong guo"),  # 完整拼音搜索
        ("我是中国人", "zhong1 guo2"),  # 带声调的拼音搜索（应该仍然匹配）
    ]

    for source, target in test_cases:
        result = search_entry(source, target)
        print(f"Source: {source}")
        print(f"Target: {target}")
        print(f"Result: {result}")
        print()

# Run the test
if __name__ == "__main__":
    test_search()