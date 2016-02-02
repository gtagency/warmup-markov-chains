class SparseMatrix:

    def __init__(self):
        self._items = {}
        self._transpose_items = {}

    @property
    def items(self):
        return self._items

    @property
    def transpose_items(self):
        return self._transpose_items

    def add(self, item, row, col, operator = lambda x, y: x):
        if row in self.items:
            if col in self.items[row]:
                self.items[row].update(\
                {col : operator(self.items[row][col], item)})
            else:
                self.items[row].update({col : item})
        else:
            self.items.update({row : {col : item}})
        if col in self.transpose_items:
            if row in self.transpose_items[col]:
                self.transpose_items[col].update(\
                {row : operator(self.transpose_items[col][row], item)})
            else:
                self.transpose_items[col].update({row : item})
        else:
            self.transpose_items.update({col : {row : item}})

    def remove(self, row, col):
        del self.items[row][col]
        del self.transpose_items[col][row]

    def __mul__(self, other_matrix):
        result = SparseMatrix()
        other_t = other_matrix.transpose_items
        for row in self.items.keys():
            for col in other_t.keys():
                cur = 0
                for entry in self.items[row].keys():
                    if entry in other_t[col]:
                        cur += self.items[row][entry] \
                               * other_t[col][entry]
                result.add(cur, row, col)
        return result

    def __add__(self, other_matrix):
        result = SparseMatrix()
        for row in other_matrix.items.keys():
            for col in other_matrix.items[row].keys():
                result.add(other_matrix.items[row][col], row, col)
        for row in self.items.keys():
            for col in self.items[row].keys():
                result.add(self.items[row][col], row, col, lambda x, y: x + y)
        return result

    def markov_chain(self, vector, iterations = 100000):
        prev = vector
        for i in range(iterations):
            cur = self * prev
            #returns at steady state
            if prev == cur:
                print(i)
                return cur
            prev = cur
        return cur

    def row(self, n):
        return self._items[n]

    def col(self, n):
        return self.transpose_items[n]

    def set_row(self, n, row):
        temp = self.items[n].copy()
        for col in temp.keys():
            self.remove(n, col)
        for col in row.keys():
            self.add(row[col], n, col, lambda x, y: y)
        return self

    def set_col(self, n, col):
        temp = self.transpose_items[n].copy()
        for row in temp.keys():
            self.remove(row, n)
        for row in col.keys():
            self.add(col[row], row, n, lambda x, y: y)
        return self

    def transpose(self):
        result = SparseMatrix()
        for row in self.items.keys():
            for col in self.items[row].keys():
                result.add(self.items[row][col], col, row)
        return result

    def row_sum(self, col):
        return sum([self.items[row][col] for row in self.items[col]])

    def col_sum(self, col):
        return sum([self.transpose_items[col][row] \
            for row in self.transpose_items[col]])

    def probabilize_col(self, col):
        result = {}
        divisor = self.col_sum(col)
        for row in self.col(col).keys():
            result.update({row : self.col(col)[row] / divisor})
        self.set_col(col, result)
        return self

    def probabilize(self):
        for col in self.transpose_items.keys():
            self.probabilize_col(col)
        return self

    def copy(self):
        result = SparseMatrix()
        for row in self.items.keys():
            for col in self.items[row].keys():
                result.add(self.items[row][col], row, col)
        return result

    def clean(self):
        for row in self.items.keys():
            for col in self.items[row].keys():
                if self.items[row][col] == 0:
                    self.remove(row, col)
        return self

    def __str__(self):
        result = []
        for row in self.items.keys():
            result.append(str(row) + ' | ')
            for col in self.items[row].keys():
                result.append(str(col) + ': ' + str(self.items[row][col]) + ' | ')
            result.append('\n')
        return ''.join(result)

    def __eq__(self, other):
        try:
            for row in self.items.keys():
                for col in self.items[row].keys():
                    if abs(self.items[row][col] - other.items[row][col]) > 1e-16:
                        return False
            return True
        except:
            return False


a = SparseMatrix()
a.add(1, 'green', 2)
a.add(2, 'green', 4)
a.add(5, 2, 'green')
a.add(1, 2, 2)
a.add(3, 1, 1)
q = a.transpose() * a
a.set_col(2, {'a' : 1, 'b' : 2})
a.probabilize_col(2)
print(a.transpose())
print(q)


b =SparseMatrix()
b.add(3, 0, 0)
b.add(1, 0, 1)
b.add(7, 1, 0)
b.add(9, 1, 1)
b.add(1, 2, 1)
b.add(3, 2, 2)
b.add(99, 1, 200000)
b.add(1, 0, 2)
b.add(110, 2, 0)
print(b)
c = b.copy().probabilize()
print("H" + str(c))
d = SparseMatrix()
d.add(1, 0, 0)
d.add(0, 1, 0)
d.add(0, 200000, 0)
d.probabilize()
print(d)

print(c.markov_chain(d, 1000))


'''
c = SparseMatrix()
c.add(0.2, 0, 0)
c.add(0.8, 1, 0)
print(c)

print(b * c)
print(b * b * c)
print(b * b * b* c)
result = c
for i in range(1000):
    result = b * result
print(result)
'''
