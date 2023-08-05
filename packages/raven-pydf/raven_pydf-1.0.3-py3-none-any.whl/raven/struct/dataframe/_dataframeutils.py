# Copyright (C) 2021 Raven Computing
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
Provides internal utility functions for DataFrame operations.
"""

import numpy as np

import raven.struct.dataframe.core as dataframe
import raven.struct.dataframe.column as column
import raven.struct.dataframe.bytecolumn as bytecolumn
import raven.struct.dataframe.shortcolumn as shortcolumn
import raven.struct.dataframe.intcolumn as intcolumn
import raven.struct.dataframe.longcolumn as longcolumn
import raven.struct.dataframe.floatcolumn as floatcolumn
import raven.struct.dataframe.doublecolumn as doublecolumn
import raven.struct.dataframe.stringcolumn as stringcolumn
import raven.struct.dataframe.charcolumn as charcolumn
import raven.struct.dataframe.booleancolumn as booleancolumn
import raven.struct.dataframe.binarycolumn as binarycolumn

# pylint: disable=C0103, R1702, R1705, R0911, R0912, R0914, R0915, W0212

def copy_of(df):
    """Creates and returns a copy of the given DataFrame

    Args:
        df: The DataFrame instance to copy

    Returns:
        A copy of the specified DataFrame or None if the argument is None
    """
    if df is None:
        return None

    copy = None
    if df.is_nullable():
        copy = dataframe.NullableDataFrame()
    else:
        copy = dataframe.DefaultDataFrame()

    df.flush()
    for col in df:
        copy.add_column(col.clone())

    if df.has_column_names():
        copy.set_column_names(df.get_column_names())

    return copy

def like(df):
    """Creates and returns a DataFrame which has the same column structure
    and Column names as the specified DataFrame instance but is otherwise empty

    Args:
        df: The DataFrame from which to copy the Column structure

    Returns:
        A DataFrame with the same Column structure and names as the
        specified DataFrame, or None if the specified DataFrame is None
    """
    if df is None:
        return None

    col = df.columns()
    if col == 0:
        return (dataframe.NullableDataFrame()
                if df.is_nullable()
                else dataframe.DefaultDataFrame())

    cols = [None] * col
    for i in range(col):
        cols[i] = column.Column.of_type(df.get_column(i).type_code())

    result = (dataframe.NullableDataFrame(cols)
              if df.is_nullable()
              else dataframe.DefaultDataFrame(cols))

    if df.has_column_names():
        result.set_column_names(df.get_column_names())

    return result

def is_numeric_fp(col):
    """Indicates whether the specified Column has a type name
    of float or double.

    Args:
        col: The Column to check

    Returns:
        A bool which indicates whether the specified Column is
        a FloatColumn, NullableFloatColumn, DoubleColumn,
        NullableDoubleColumn
    """
    return col.type_code() in (floatcolumn.FloatColumn.TYPE_CODE,
                               floatcolumn.NullableFloatColumn.TYPE_CODE,
                               doublecolumn.DoubleColumn.TYPE_CODE,
                               doublecolumn.NullableDoubleColumn.TYPE_CODE)

def merge(*dataframes):
    """Merges all given DataFrame instances into one DataFrame.

    All DataFames are merged by columns. All DataFrames must have an
    equal number of rows but may be of any type. All columns are added to
    the returned DataFrame in the order of the arguments passed to this
    method. Only passing one DataFrame to this method will simply
    return that instance.

    Columns with duplicate names are included in the returned DataFrame
    and a postfix is added to each duplicate column name.
    All columns of the returned DataFrame are backed by their origin,
    which means that changes to the original DataFrame are reflected in
    the merged DataFrame and vice versa. This does not apply, however,
    if columns need to be converted to a nullable type. For example, if
    one DataFrame argument is nullable, then all columns from non-nullable
    DataFrame arguments are converted to their corresponding
    nullable equivalent.

    If columns should be independent from their origin, then simply pass
    a clone (copy) of each DataFrame argument to this method.

    Example:
        merged = DataFrame.merge(DataFrame.copy(df1), DataFrame.copy(df2))

    Args:
        dataframes: The DataFrames to be merged

    Returns:
        A DataFrame composed of all columns of the given DataFrames
    """
    if dataframes is None or len(dataframes) == 0:
        raise dataframe.DataFrameException("Arg must not be None or empty")

    if len(dataframes) == 1:
        return dataframes[0]

    rows = dataframes[0].rows()
    cols = 0
    has_nullable = False
    has_names = False
    for i, df in enumerate(dataframes):
        if df is None:
            raise dataframe.DataFrameException(
                "DataFrame argument must not be None")

        cols += df.columns()
        if df.rows() != rows:
            raise dataframe.DataFrameException(
                ("Size missmatch for DataFrame argument at index {}. "
                 "Expected {} rows but found {}")
                .format(i, rows, df.rows()))

        if df.is_nullable():
            has_nullable = True

        if df.has_column_names():
            has_names = True

    for _, df in enumerate(dataframes):
        df.flush()

    names = None
    if has_names:
        names = [None] * cols
        for i in range(cols):
            names[i] = str(i)

        k = 0
        for i, df in enumerate(dataframes):
            for j in range(df.columns()):
                c = df.get_column(j)
                if c.get_name():
                    names[k] = c.get_name()
                k += 1

        for i in range(cols):
            k = 0
            already_set = False
            n = names[i]
            for j in range(cols):
                if i != j:
                    if n == names[j]:
                        if not already_set:
                            names[i] = names[i] + "_" + str(k)
                            k += 1
                            already_set = True

                        names[j] = names[j] + "_" + str(k)
                        k += 1

    columns = [None] * cols
    k = 0
    for i, df in enumerate(dataframes):
        for j in range(df.columns()):
            if has_nullable:
                columns[k] = df.get_column(j).as_nullable()
                k += 1
            else:
                columns[k] = df.get_column(j)
                k += 1

    merged = None
    if has_nullable:
        merged = dataframe.NullableDataFrame(columns)
    else:
        merged = dataframe.DefaultDataFrame(columns)

    if has_names:
        merged.set_column_names(names)

    return merged

def convert(df, target_type):
    """Converts the given DataFrame from a DefaultDataFrame to a NullableDataFrame
    or vice versa.

    Converting a DefaultDataFrame to a NullableDataFrame will not change
    any internal values, except that now you can add/insert null values to it.
    Converting a NullableDataFrame to a DefaultDataFrame will convert all None
    occurrences to the primitive defaults according to the Column they are located.

    Args:
        df: The DataFrame instance to convert. Must not be None
        target_type: The type to convert the given DataFrame to.
            May be 'default' or 'nullable'

    Returns:
        A DataFrame converted from the type of the argument passed to this method
        to the type specified
    """
    if df is None or target_type is None:
        raise ValueError("Arg must not be null")

    if not isinstance(target_type, str):
        raise ValueError("Target type argument must be specified as a string")

    target_type = target_type.lower()
    if target_type not in ("defaultdataframe", "default", "nullabledataframe", "nullable"):
        raise ValueError("Unable to convert to '" + str(target_type)
                         + "'. Must be either 'default' or 'nullable'")

    if target_type == "defaultdataframe":
        target_type = "default"
    elif target_type == "nullabledataframe":
        target_type = "nullable"

    source_type = "nullable" if df.is_nullable() else "default"
    if target_type == source_type:
        return copy_of(df)

    rows = df.rows()
    converted = None
    # convert from Nullable to Default
    if target_type == "default":
        converted = dataframe.DefaultDataFrame()
        for col in df:
            tc = col.type_code()
            if tc == bytecolumn.NullableByteColumn.TYPE_CODE:
                vals = np.array([0] * rows, dtype=np.int8)
                for i in range(rows):
                    val = col.get_value(i)
                    vals[i] = 0 if val is None else val

                converted.add_column(bytecolumn.ByteColumn(col.get_name(), vals))
            elif tc == shortcolumn.NullableShortColumn.TYPE_CODE:
                vals = np.array([0] * rows, dtype=np.int16)
                for i in range(rows):
                    val = col.get_value(i)
                    vals[i] = 0 if val is None else val

                converted.add_column(shortcolumn.ShortColumn(col.get_name(), vals))
            elif tc == intcolumn.NullableIntColumn.TYPE_CODE:
                vals = np.array([0] * rows, dtype=np.int32)
                for i in range(rows):
                    val = col.get_value(i)
                    vals[i] = 0 if val is None else val

                converted.add_column(intcolumn.IntColumn(col.get_name(), vals))
            elif tc == longcolumn.NullableLongColumn.TYPE_CODE:
                vals = np.array([0] * rows, dtype=np.int64)
                for i in range(rows):
                    val = col.get_value(i)
                    vals[i] = 0 if val is None else val

                converted.add_column(longcolumn.LongColumn(col.get_name(), vals))
            elif tc == stringcolumn.NullableStringColumn.TYPE_CODE:
                vals = np.array([None] * rows, dtype=np.object)
                for i in range(rows):
                    val = col.get_value(i)
                    vals[i] = (stringcolumn.StringColumn.DEFAULT_VALUE
                               if val is None or val == ""
                               else val)

                converted.add_column(stringcolumn.StringColumn(col.get_name(), vals))
            elif tc == floatcolumn.NullableFloatColumn.TYPE_CODE:
                vals = np.array([0.0] * rows, dtype=np.float32)
                for i in range(rows):
                    val = col.get_value(i)
                    vals[i] = 0.0 if val is None else val

                converted.add_column(floatcolumn.FloatColumn(col.get_name(), vals))
            elif tc == doublecolumn.NullableDoubleColumn.TYPE_CODE:
                vals = np.array([0.0] * rows, dtype=np.float64)
                for i in range(rows):
                    val = col.get_value(i)
                    vals[i] = 0 if val is None else val

                converted.add_column(doublecolumn.DoubleColumn(col.get_name(), vals))
            elif tc == charcolumn.NullableCharColumn.TYPE_CODE:
                vals = np.array([0] * rows, dtype=np.uint8)
                default_val = ord(charcolumn.CharColumn.DEFAULT_VALUE)
                for i in range(rows):
                    val = col._values[i]
                    vals[i] = default_val if val is None else val

                converted.add_column(charcolumn.CharColumn(col.get_name(), vals))
            elif tc == booleancolumn.NullableBooleanColumn.TYPE_CODE:
                vals = np.array([False] * rows, dtype=np.bool)
                for i in range(rows):
                    val = col.get_value(i)
                    vals[i] = False if val is None else val

                converted.add_column(booleancolumn.BooleanColumn(col.get_name(), vals))
            elif tc == binarycolumn.NullableBinaryColumn.TYPE_CODE:
                vals = np.array([None] * rows, dtype=np.object)
                for i in range(rows):
                    val = col.get_value(i)
                    vals[i] = bytearray.fromhex("00") if val is None else val

                converted.add_column(binarycolumn.BinaryColumn(col.get_name(), vals))
            else: # undefined type
                raise dataframe.DataFrameException(
                    ("Unable to convert dataframe. Unrecognized "
                     "column type {}".format(type(col))))

    else: # convert from Default to Nullable
        converted = dataframe.NullableDataFrame()
        for col in df:
            tc = col.type_code()
            vals = np.array([None] * rows, dtype=np.object)
            for i in range(rows):
                vals[i] = col.get_value(i)

            if tc == bytecolumn.ByteColumn.TYPE_CODE:
                converted.add_column(bytecolumn.NullableByteColumn(col.get_name(), vals))
            elif tc == shortcolumn.ShortColumn.TYPE_CODE:
                converted.add_column(shortcolumn.NullableShortColumn(col.get_name(), vals))
            elif tc == intcolumn.IntColumn.TYPE_CODE:
                converted.add_column(intcolumn.NullableIntColumn(col.get_name(), vals))
            elif tc == longcolumn.LongColumn.TYPE_CODE:
                converted.add_column(longcolumn.NullableLongColumn(col.get_name(), vals))
            elif tc == stringcolumn.StringColumn.TYPE_CODE:
                converted.add_column(stringcolumn.NullableStringColumn(col.get_name(), vals))
            elif tc == floatcolumn.FloatColumn.TYPE_CODE:
                converted.add_column(floatcolumn.NullableFloatColumn(col.get_name(), vals))
            elif tc == doublecolumn.DoubleColumn.TYPE_CODE:
                converted.add_column(doublecolumn.NullableDoubleColumn(col.get_name(), vals))
            elif tc == charcolumn.CharColumn.TYPE_CODE:
                converted.add_column(charcolumn.NullableCharColumn(col.get_name(), vals))
            elif tc == booleancolumn.BooleanColumn.TYPE_CODE:
                converted.add_column(booleancolumn.NullableBooleanColumn(col.get_name(), vals))
            elif tc == binarycolumn.BinaryColumn.TYPE_CODE:
                converted.add_column(binarycolumn.NullableBinaryColumn(col.get_name(), vals))
            else: # undefined type
                raise dataframe.DataFrameException(
                    ("Unable to convert dataframe. Unrecognized "
                     "column type {}".format(type(col))))

    return converted

def column_from_typename(typename):
    """Constructs and returns a Column from the specified typename.

    The returned Column instance is a default (non-nullable) Column.

    Args:
        typename: The type name of the Column to return, as a str

    Returns:
        A Column instance from the specified type name,
        or None if the argument is not a valid type name
    """
    if typename == "byte":
        return bytecolumn.ByteColumn()
    elif typename == "short":
        return shortcolumn.ShortColumn()
    elif typename in ("int", "integer"):
        return intcolumn.IntColumn()
    elif typename == "long":
        return longcolumn.LongColumn()
    elif typename in ("string", "str"):
        return stringcolumn.StringColumn()
    elif typename == "float":
        return floatcolumn.FloatColumn()
    elif typename == "double":
        return doublecolumn.DoubleColumn()
    elif typename in ("char", "character"):
        return charcolumn.CharColumn()
    elif typename in ("boolean", "bool"):
        return booleancolumn.BooleanColumn()
    elif typename == "binary":
        return binarycolumn.BinaryColumn()
    else:
        return None

def join(df1, col1, df2, col2):
    """Combines all rows from the specified DataFrames which have matching
    values in their columns with the corresponding specified name.

    Both DataFrames must have a column with the corresponding specified name
    and an identical element type. All columns in both DataFrame instances must
    be labeled by the time this method is called. The specified DataFrames may be
    of any types.

    All Columns in the second DataFrame argument that are also existent in
    the first DataFrame argument are excluded in the result DataFrame returned
    by this method. Therefore, in the case of duplicate Columns, the returned
    DataFrame only contains the corresponding Column from the first DataFrame.

    Args:
        df1: The first DataFrame to join. Must not be None
        col1: The name of the Column in the first DataFrame argument
            to match values for. Must be a str
        df2: The second DataFrame to join. Must not be None
        col2: The name of the Column in the second DataFrame argument
            to match values for. Must be a str

    Returns:
        A DataFrame with joined rows from both specified DataFrames
        that have matching values in the Columns with the specified names
    """
    if df1 is None or df2 is None:
        raise dataframe.DataFrameException("DataFrame argument must not be None")

    if df1 is df2:
        raise dataframe.DataFrameException("Join operation is self-referential")

    if not col1:
        raise dataframe.DataFrameException(
            "First column name argument must not be None or empty")

    if not col2:
        raise dataframe.DataFrameException(
            "Second column name argument must not be None or empty")

    if not df1.has_column_names():
        raise dataframe.DataFrameException("DataFrame must has column labels")

    if not df2.has_column_names():
        raise dataframe.DataFrameException("DataFrame argument must have column labels")

    if not df2.has_column(col2):
        raise dataframe.DataFrameException(
            "Invalid column name for DataFrame argument: '{}'".format(col2))

    if df1.get_column(col1).type_name() != df2.get_column(col2).type_name():
        raise dataframe.DataFrameException(
            ("Column '{}' in DataFrame argument has "
             "a different type. "
             "Expected {} but found {}").format(
                 df2.get_column(col2).get_name(),
                 df1.get_column(col1).type_name(),
                 df2.get_column(col2).type_name()))

    # create a set holding the names of all columns from df2
    # that should be bypassed in the result because they already exist in df1
    duplicates = set()
    names = df2.get_column_names()
    for _, n in enumerate(names):
        if df1.has_column(n):
            duplicates.add(n)

    # add the specified column name to make sure
    # it is not included in the below computations
    duplicates.add(col2)
    df1.flush()
    df2.flush()
    # find the elements common to both DataFrames
    intersec = df1.get_columns(col1).intersection_rows(df2.get_columns(col2))
    use_nullable = df1.is_nullable() or df2.is_nullable()
    result = (dataframe.NullableDataFrame() if use_nullable
              else dataframe.DefaultDataFrame())

    # add all columns from df1
    for i in range(df1.columns()):
        c = column.Column.of_type(df1.get_column(i).type_code())
        result.add_column(col=c.as_nullable() if use_nullable else c,
                          name=df1.get_column(i).get_name())

    # add all columns from df2 as long as they are not already in df1
    for i in range(df2.columns()):
        col = df2.get_column(i)
        # if the column is in the collection, then it
        # is either 'col2' or another duplicate, so it is skipped
        if not col.get_name() in duplicates:
            c = column.Column.of_type(col.type_code())
            result.add_column(col=c.as_nullable() if use_nullable else c,
                              name=col.get_name())

    # iterate over all common elements and add all rows to
    # the result from both DataFrames that match the common
    # element in their respective key column
    for i in range(intersec.rows()):
        filter_key = str(intersec.get_column(0).get_value(i))
        filter1 = df1.filter(col1, filter_key)
        filter2 = df2.filter(col2, filter_key)
        # remove 'col2' and any column already existent in df1
        for name in duplicates:
            filter2.remove_column(name)

        length_col1 = df1.columns()
        length_col2 = df2.columns() - len(duplicates)
        # reuse the row list
        length_row = length_col1 + length_col2
        row = [None] * length_row
        for j in range(filter1.rows()):
            for k in range(filter2.rows()):
                for l in range(length_col1):
                    row[l] = filter1.get_column(l).get_value(j)

                for l in range(length_col2):
                    row[length_col1 + l] = filter2.get_column(l).get_value(k)

                result.add_row(row)

    result.flush()
    return result

def _group_operation(df, col, operation):
    """Performs a group_by operation for the specified DataFrame and Column.

    Operation codes:
    * 1 = Minimum
    * 2 = Maximum
    * 3 = Average
    * 4 = Sum

    Args:
        df: The DataFrame to use for the group operation
        col: The Column to use for the group operation
        operation: The operation code to use

    Returns:
        A DataFrame representing the result of the group operation
    """
    if df._internal_next() == -1 or col < 0 or col >= df.columns():
        raise dataframe.DataFrameException("Invalid column index: {}".format(col))

    c = df.get_column(col)
    n_numeric = 0
    for i in range(df.columns()):
        c_i = df.get_column(i)
        if not c_i._name:
            raise dataframe.DataFrameException(
                "All columns must be labeled for group operations")

        if c_i is not c and c_i.is_numeric():
            n_numeric += 1

    uniques = df.unique(col)
    n_uniques = len(uniques)
    contains_null = df.contains(col, "None") if df.is_nullable() else False
    col_length = n_uniques + 1 if contains_null else n_uniques
    cols = [None] * (n_numeric + 1)
    col_names = [None] * (n_numeric + 1)
    cols[0] = column.Column.of_type(c.type_code(), col_length)
    col_names[0] = c._name
    n_numeric = 1
    for i in range(df.columns()):
        c_i = df.get_column(i)
        if c_i is not c and c_i.is_numeric():
            if operation in (3, 4): # average or sum op
                cols[n_numeric] = (doublecolumn.NullableDoubleColumn(values=col_length)
                                   if df.is_nullable()
                                   else doublecolumn.DoubleColumn(values=col_length))

            else:
                cols[n_numeric] = column.Column.of_type(c_i.type_code(), col_length)

            col_names[n_numeric] = c_i._name
            n_numeric += 1

    result = (dataframe.NullableDataFrame(cols)
              if df.is_nullable()
              else dataframe.DefaultDataFrame(cols))

    result.set_column_names(col_names)

    length = len(cols)
    index = 0
    for elem in uniques:
        row = [None] * length
        row[0] = elem
        filtered = df.filter(c._name, str(elem))
        for i in range(1, length, 1):
            value = 0.0
            if operation == 1:
                value = filtered.minimum(col_names[i])
            elif operation == 2:
                value = filtered.maximum(col_names[i])
            elif operation == 3:
                value = filtered.average(col_names[i])
            elif operation == 4:
                value = filtered.sum(col_names[i])
            else:
                raise dataframe.DataFrameException(
                    "Unknown group operation: {}".format(operation))

            row[i] = _cast_to_numeric_type(cols[i], value)

        result.set_row(index, row)
        index += 1

    if contains_null:
        row = [None] * length
        row[0] = None
        filtered = df.filter(c._name, "None")
        for i in range(1, length, 1):
            value = 0.0
            if operation == 1:
                value = filtered.minimum(col_names[i])
            elif operation == 2:
                value = filtered.maximum(col_names[i])
            elif operation == 3:
                value = filtered.average(col_names[i])
            elif operation == 4:
                value = filtered.sum(col_names[i])
            else:
                raise dataframe.DataFrameException(
                    "Unknown group operation: {}".format(operation))

            row[i] = _cast_to_numeric_type(cols[i], value)

        result.set_row(index, row)
        index += 1

    return result

def _cast_to_numeric_type(col, value):
    """Casts the specified double to the corresponding Number
    type of the specified Column.

    Args:
        col: The Column which specifies the numeric type
        value: The float value to cast

    Returns:
        A number which has the concrete type used
        by the specified Column
    """
    c = col.type_code()
    if col.is_nullable():
        if c == doublecolumn.NullableDoubleColumn.TYPE_CODE:
            return float(value)
        elif c == floatcolumn.NullableFloatColumn.TYPE_CODE:
            return float(value)
        elif c == bytecolumn.NullableByteColumn.TYPE_CODE:
            return int(value) if not np.isnan(value) else None
        elif c == shortcolumn.NullableShortColumn.TYPE_CODE:
            return int(value) if not np.isnan(value) else None
        elif c == intcolumn.NullableIntColumn.TYPE_CODE:
            return int(value) if not np.isnan(value) else None
        elif c == longcolumn.NullableLongColumn.TYPE_CODE:
            return int(value) if not np.isnan(value) else None
        else:
            raise dataframe.DataFrameException("Unrecognized column type")
    else:
        if c == doublecolumn.DoubleColumn.TYPE_CODE:
            return float(value)
        elif c == floatcolumn.FloatColumn.TYPE_CODE:
            return float(value)
        elif c == bytecolumn.ByteColumn.TYPE_CODE:
            return int(value)
        elif c == shortcolumn.ShortColumn.TYPE_CODE:
            return int(value)
        elif c == intcolumn.IntColumn.TYPE_CODE:
            return int(value)
        elif c == longcolumn.LongColumn.TYPE_CODE:
            return int(value)
        else:
            raise dataframe.DataFrameException("Unrecognized column type")
