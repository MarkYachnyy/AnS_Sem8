def str_to_int(S, A):
    char_pos = {}
    for i in range(len(A)):
        char_pos[A[i]] = i
    res = []
    for c in S:
        res.append(char_pos[c])
    return res


class Arc:
    def __init__(self):
        self.i_beg = -1
        self.i_end = -1
        self.dest_vert = None
        self.src_vert = None
        self.i_dest_vert = -1


class Node:
    def __init__(self, nA):
        self.arcs = [None for _ in range(nA)]
        self.s_ref = None
        self.arc_in = None


def init_vert(nA, arc_in):
    res = Node(nA)
    res.arc_in = arc_in
    return res


def init_arc(src_node: Node = None, ch_arc_code=0, i_beg=-1, i_end=-1, dest_vert=None, i_dest_vert=None):
    arc = Arc()
    arc.i_beg = i_beg
    arc.i_end = i_end
    src_node.arcs[ch_arc_code] = arc
    arc.dest_vert = dest_vert
    arc.i_dest_vert = i_dest_vert
    arc.src_vert = src_node
    return arc


def find_suffix_tree_arc(str, substr, m_same, tree):
    m = len(substr)
    arc = None
    idx_substr, idx_arc = 0, 0
    curr_node = tree
    stopped = False
    while not stopped and curr_node:
        next_arc = curr_node.arcs[substr[idx_substr]]
        if next_arc:
            arc = next_arc
            idx_arc = arc.i_beg
            same_rest = m_same - idx_substr
            if same_rest > 0:
                arc_len = arc.i_end - arc.i_beg + 1
                if same_rest <= arc_len:
                    idx_substr = m_same - 1
                    idx_arc += same_rest - 1
                else:
                    idx_substr += arc_len
                    idx_arc = arc.i_end + 1
                    curr_node = arc.dest_vert
                    continue
            idx_substr += 1
            idx_arc += 1
            while idx_substr < m and idx_arc < arc.i_end + 1 and substr[idx_substr] == str[idx_arc]:
                idx_substr += 1
                idx_arc += 1
            if idx_arc <= arc.i_end:
                stopped = True
            else:
                curr_node = arc.dest_vert
        else:
            stopped = True
    # if idx_substr == m:
    #     idx_arc += 1
    return arc, idx_substr, idx_arc


def top_jump_bottom(str, substr, arc, i_arc_end, idx_substr, idx_arc):
    m = len(substr)
    if not arc:
        return None, idx_substr, idx_arc
    arc_next = None
    src_vert = None
    is_inner_vert = arc.dest_vert and idx_arc > i_arc_end
    if is_inner_vert:
        src_vert = arc.dest_vert
    else:
        src_vert = arc.src_vert
    ref_vert = src_vert.s_ref
    if not ref_vert:
        ref_vert = src_vert

    n_chars_up = 1 if is_inner_vert else idx_arc - arc.i_beg + 1

    if not src_vert.s_ref:
        n_chars_up -= 1
    n_vert_chr = m - n_chars_up
    arc_next, idx_substr, idx_arc = find_suffix_tree_arc(str, substr[n_vert_chr:], n_chars_up-1, ref_vert)

    if not arc_next:
        arc_next = ref_vert.arc_in
        if arc_next:
            idx_arc = arc_next.i_end + 1

    idx_substr += n_vert_chr
    return arc_next, idx_substr, idx_arc


def st_build_online_n2(str, nA):
    n = len(str)
    tree = init_vert(nA=nA, arc_in=None)
    init_arc(src_node=tree, ch_arc_code=str[0], i_beg=0, i_end=0, dest_vert=None, i_dest_vert=0)
    for i in range(n):
        arc_prev: Arc = None
        i_end_prev = -1
        ref_from = None
        idx_substr = 0
        idx_arc = 0
        for j in range(i + 1):
            m = i - j + 1
            if j:
                uv_arc, idx_substr, idx_arc = top_jump_bottom(str, str[j:], arc_prev, i_end_prev, idx_substr, idx_arc)
            else:
                uv_arc, idx_substr, idx_arc = find_suffix_tree_arc(str, str[j:], m-1, tree)
            arc_prev = uv_arc
            i_end_prev = arc_prev.i_end if arc_prev else -1
            if idx_substr == m:
                if ref_from:
                    ref_from.s_ref = uv_arc.src_vert
                ref_from = None
                idx_arc-=1
                continue
            w_node = None
            if not uv_arc:
                w_node = tree
            else:
                w_node = uv_arc.dest_vert
            if not w_node and idx_arc > uv_arc.i_end:
                uv_arc.i_end += 1
                ref_from = None
                continue

            if uv_arc and idx_arc <= uv_arc.i_end:
                w_node = init_vert(nA=nA, arc_in=uv_arc)
                wv_arc = init_arc(w_node, str[idx_arc], idx_arc, uv_arc.i_end, uv_arc.dest_vert, uv_arc.i_dest_vert)
                if uv_arc.dest_vert:
                    uv_arc.dest_vert.arc_in = wv_arc

                uv_arc.dest_vert = w_node
                uv_arc.i_dest_vert = -1
                uv_arc.i_end = idx_arc-1

                if ref_from:
                    ref_from.s_ref = w_node

                ref_from = w_node
            else:
                if ref_from:
                    ref_from.s_ref = w_node
                ref_from = None

            init_arc(w_node, str[i], i, i, None, j)

    return tree

s = 'ABRACADABRA$'
int_str = str_to_int(s, 'ABCDR$')

tree = st_build_online_n2(int_str, 6)


def print_tree(node, level=0, label_prefix=""):
    """
    Рекурсивно печатает суффиксное дерево, начиная с указанного узла.

    Args:
        node: начальный узел для печати
        level: уровень вложенности (для отступов)
        label_prefix: префикс метки от корня до текущего узла
    """
    if node is None:
        return

    # Печатаем информацию о текущем узле
    indent = "  " * level
    if level == 0:
        print(f"{indent}Корневой узел:")
    else:
        print(f"{indent}Узел (s_ref: {id(node.s_ref) if node.s_ref else None}):")

    # Проходим по всем дугам из текущего узла
    for i, arc in enumerate(node.arcs):
        if arc is not None:
            # Формируем информацию о дуге
            arc_info = f"[{arc.i_beg}, {arc.i_end}]"

            # Печатаем дугу
            print(f"{indent}  Дуга {i}: {arc_info} -> ", end="")

            if arc.dest_vert is not None:
                print(f"узел {id(arc.dest_vert)}")
                # Рекурсивно печатаем поддерево
                new_prefix = label_prefix + arc_info
                print_tree(arc.dest_vert, level + 1, new_prefix)
            else:
                print("терминальный узел")


def print_tree_with_string(node, s, level=0):
    """
    Печатает суффиксное дерево с отображением фактических подстрок.

    Args:
        node: начальный узел для печати
        s: исходная строка, по которой построено дерево
        level: уровень вложенности (для отступов)
    """
    if node is None:
        return

    indent = "  " * level
    if level == 0:
        print(f"{indent}Корневой узел:")
    else:
        print(f"{indent}Узел (s_ref: {id(node.s_ref) if node.s_ref else None}):")

    for i, arc in enumerate(node.arcs):
        if arc is not None:
            # Получаем фактическую подстроку для дуги
            if arc.i_end == -1:  # До конца строки
                substring = s[arc.i_beg:]
                arc_info = f"[{arc.i_beg}, конец] = '{substring}'"
            else:
                substring = s[arc.i_beg:arc.i_end + 1]
                arc_info = f"[{arc.i_beg}, {arc.i_end}] = '{substring}'"

            print(f"{indent}  Дуга {i}: {arc_info} -> ", end="")

            if arc.dest_vert is not None:
                print(f"узел {id(arc.dest_vert)}")
                print_tree_with_string(arc.dest_vert, s, level + 1)
            else:
                print("терминальный узел")