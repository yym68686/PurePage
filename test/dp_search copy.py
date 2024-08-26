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