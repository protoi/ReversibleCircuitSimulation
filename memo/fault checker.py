"""
Greedy way of finding a complete test set

"""

table = [
  {
    "smgf": [],
    "pmgf": [
      18,
      19,
      20,
      35,
      40,
      41,
      42,
      43,
      44
    ],
    "mmgf": []
  },
  {
    "smgf": [
      1,
      3,
      5,
      6,
      7,
      8,
      11,
      12,
      14,
      16
    ],
    "pmgf": [
      19,
      22,
      33,
      35,
      40,
      42,
      44
    ],
    "mmgf": [
      45,
      46,
      47,
      48,
      49,
      50,
      51,
      52,
      53,
      54,
      55,
      56,
      57,
      58,
      59,
      60,
      61,
      62,
      63,
      64,
      65,
      66,
      67,
      68,
      69,
      70,
      71,
      72,
      73,
      74,
      75,
      76,
      77,
      78,
      79,
      80,
      81,
      82,
      83,
      84,
      85,
      86,
      87,
      88,
      89,
      90,
      92,
      93,
      94,
      95,
      96,
      97,
      98,
      99,
      100,
      101,
      102,
      104,
      105,
      106,
      107,
      108,
      109,
      110,
      111,
      112,
      113,
      114,
      116,
      117,
      118,
      120,
      121,
      122,
      123,
      124,
      125,
      126,
      127,
      128,
      129,
      130,
      131,
      132,
      133,
      134,
      135,
      136,
      137,
      139,
      140,
      141,
      142,
      143,
      144,
      146,
      149,
      150,
      151,
      152,
      153,
      156,
      157,
      158,
      159,
      162,
      163,
      164,
      165,
      166,
      167,
      168,
      169,
      170,
      171,
      172,
      173,
      174,
      175,
      176,
      177,
      178,
      179,
      180
    ]
  },
  {
    "smgf": [
      2,
      3,
      10,
      13
    ],
    "pmgf": [
      18,
      22,
      24,
      29,
      34,
      36,
      38,
      41,
      42,
      43,
      44
    ],
    "mmgf": [
      45,
      46,
      47,
      48,
      49,
      50,
      51,
      52,
      53,
      54,
      55,
      56,
      57,
      58,
      59,
      60,
      61,
      62,
      63,
      64,
      65,
      66,
      67,
      68,
      69,
      70,
      71,
      72,
      73,
      74,
      75,
      76,
      77,
      78,
      79,
      80,
      81,
      82,
      83,
      84,
      85,
      86,
      87,
      88,
      89,
      95,
      96,
      97,
      107,
      108,
      109,
      118,
      119,
      120,
      128,
      129,
      130,
      137,
      138,
      139,
      145,
      146,
      147,
      153,
      154,
      161,
      162,
      163,
      164,
      165,
      166,
      167,
      168,
      169,
      170,
      171,
      172,
      173,
      174
    ]
  },
  {
    "smgf": [
      1,
      2,
      14
    ],
    "pmgf": [
      20,
      23,
      25,
      28,
      32,
      35,
      37,
      39,
      40,
      42,
      43,
      44
    ],
    "mmgf": [
      45,
      46,
      47,
      48,
      49,
      50,
      51,
      52,
      53,
      54,
      55,
      56,
      57,
      58,
      59,
      60,
      61,
      62,
      63,
      64,
      65,
      66,
      67,
      68,
      69,
      70,
      71,
      72,
      73,
      74,
      75,
      86,
      87,
      88,
      89,
      99,
      100,
      101,
      102,
      111,
      112,
      113,
      114,
      122,
      123,
      124,
      125,
      132,
      133,
      134,
      135,
      141,
      142,
      143,
      144,
      149,
      150,
      151,
      152,
      156,
      157,
      158,
      159,
      162,
      163,
      164,
      165,
      167,
      168,
      169,
      170,
      171,
      172,
      173,
      174,
      175,
      176,
      177
    ]
  },
  {
    "smgf": [
      14,
      15,
      17
    ],
    "pmgf": [
      18,
      19,
      20,
      28,
      35,
      39,
      40,
      43
    ],
    "mmgf": [
      57,
      58,
      59,
      60,
      72,
      73,
      74,
      75,
      86,
      87,
      88,
      89,
      99,
      100,
      101,
      102,
      111,
      112,
      113,
      114,
      122,
      123,
      124,
      125,
      132,
      133,
      134,
      135,
      141,
      142,
      143,
      144,
      149,
      150,
      151,
      152,
      156,
      157,
      158,
      159,
      162,
      163,
      164,
      165,
      167,
      168,
      169,
      170,
      171,
      172,
      173,
      174,
      175,
      176,
      177,
      178,
      179,
      180
    ]
  },
  {
    "smgf": [
      1,
      3,
      5,
      9,
      10,
      13,
      16
    ],
    "pmgf": [
      19,
      22,
      27,
      29,
      31,
      41,
      42,
      44
    ],
    "mmgf": [
      45,
      46,
      47,
      48,
      49,
      50,
      51,
      52,
      53,
      54,
      55,
      56,
      57,
      58,
      59,
      60,
      61,
      62,
      63,
      64,
      65,
      66,
      67,
      71,
      72,
      73,
      74,
      75,
      76,
      77,
      78,
      79,
      80,
      81,
      85,
      86,
      87,
      88,
      89,
      90,
      91,
      92,
      93,
      94,
      95,
      96,
      97,
      98,
      99,
      100,
      101,
      102,
      103,
      104,
      105,
      106,
      107,
      108,
      109,
      110,
      111,
      112,
      113,
      114,
      117,
      118,
      119,
      120,
      121,
      122,
      123,
      124,
      125,
      127,
      128,
      129,
      130,
      131,
      132,
      133,
      134,
      135,
      136,
      137,
      138,
      139,
      140,
      141,
      142,
      143,
      144,
      145,
      146,
      147,
      148,
      149,
      150,
      151,
      152,
      153,
      154,
      158,
      159,
      161,
      162,
      163,
      164,
      165,
      166,
      167,
      168,
      169,
      170,
      171,
      172,
      173,
      174,
      176,
      177,
      178,
      179,
      180
    ]
  },
  {
    "smgf": [
      2,
      3,
      7,
      9,
      10,
      13,
      14,
      16
    ],
    "pmgf": [
      18,
      22,
      24,
      26,
      30,
      37,
      39,
      42,
      44
    ],
    "mmgf": [
      45,
      46,
      47,
      48,
      49,
      50,
      51,
      52,
      53,
      54,
      55,
      56,
      57,
      58,
      59,
      60,
      61,
      62,
      63,
      64,
      65,
      66,
      67,
      68,
      69,
      70,
      71,
      72,
      73,
      74,
      75,
      76,
      77,
      78,
      79,
      80,
      81,
      85,
      86,
      87,
      88,
      89,
      92,
      93,
      94,
      95,
      96,
      97,
      98,
      99,
      100,
      101,
      102,
      104,
      105,
      106,
      107,
      108,
      109,
      110,
      111,
      112,
      113,
      114,
      115,
      116,
      117,
      118,
      119,
      120,
      121,
      122,
      123,
      124,
      125,
      126,
      127,
      128,
      129,
      130,
      131,
      132,
      133,
      134,
      135,
      136,
      137,
      138,
      139,
      140,
      143,
      144,
      145,
      146,
      147,
      148,
      151,
      152,
      153,
      154,
      156,
      157,
      158,
      159,
      161,
      162,
      163,
      164,
      165,
      166,
      167,
      168,
      169,
      170,
      171,
      172,
      173,
      174,
      175,
      176,
      177,
      178,
      179,
      180
    ]
  },
  {
    "smgf": [
      1,
      2,
      15,
      17
    ],
    "pmgf": [
      20,
      23,
      35,
      37,
      40,
      41,
      43
    ],
    "mmgf": [
      45,
      46,
      47,
      48,
      49,
      50,
      51,
      52,
      53,
      54,
      55,
      56,
      57,
      58,
      59,
      60,
      61,
      62,
      63,
      64,
      65,
      66,
      67,
      68,
      69,
      70,
      71,
      72,
      73,
      74,
      75,
      87,
      88,
      89,
      100,
      101,
      102,
      112,
      113,
      114,
      123,
      124,
      125,
      133,
      134,
      135,
      142,
      143,
      144,
      150,
      151,
      152,
      157,
      158,
      159,
      163,
      164,
      165,
      168,
      169,
      170,
      172,
      173,
      174,
      175,
      176,
      177,
      178,
      179,
      180
    ]
  },
  {
    "smgf": [
      16
    ],
    "pmgf": [
      18,
      19,
      20,
      21,
      33,
      35,
      36,
      38,
      40,
      41,
      42,
      44
    ],
    "mmgf": [
      59,
      60,
      74,
      75,
      88,
      89,
      101,
      102,
      113,
      114,
      124,
      125,
      134,
      135,
      143,
      144,
      151,
      152,
      158,
      159,
      164,
      165,
      169,
      170,
      173,
      174,
      176,
      177,
      178,
      179,
      180
    ]
  },
  {
    "smgf": [
      1,
      3,
      4,
      7,
      10,
      12,
      14,
      15,
      16,
      17
    ],
    "pmgf": [
      19,
      24,
      26,
      34,
      36,
      40
    ],
    "mmgf": [
      45,
      46,
      47,
      48,
      49,
      50,
      51,
      52,
      53,
      54,
      55,
      56,
      57,
      58,
      59,
      60,
      61,
      65,
      66,
      67,
      70,
      71,
      72,
      73,
      74,
      75,
      79,
      80,
      81,
      84,
      85,
      86,
      87,
      88,
      89,
      90,
      91,
      92,
      93,
      94,
      95,
      96,
      97,
      98,
      99,
      100,
      101,
      102,
      104,
      105,
      106,
      109,
      110,
      111,
      112,
      113,
      114,
      115,
      116,
      117,
      120,
      121,
      122,
      123,
      124,
      125,
      126,
      127,
      130,
      131,
      132,
      133,
      134,
      135,
      137,
      138,
      139,
      140,
      141,
      142,
      143,
      144,
      145,
      146,
      147,
      148,
      149,
      150,
      151,
      152,
      153,
      154,
      155,
      156,
      157,
      158,
      159,
      160,
      161,
      162,
      163,
      164,
      165,
      166,
      167,
      168,
      169,
      170,
      171,
      172,
      173,
      174,
      175,
      176,
      177,
      179,
      180
    ]
  },
  {
    "smgf": [
      2,
      3,
      4,
      5,
      10,
      11,
      15,
      16,
      17
    ],
    "pmgf": [
      18,
      27,
      29,
      34,
      38,
      40,
      41
    ],
    "mmgf": [
      45,
      46,
      47,
      48,
      49,
      50,
      51,
      52,
      53,
      58,
      60,
      61,
      62,
      63,
      64,
      65,
      66,
      67,
      68,
      73,
      75,
      77,
      78,
      79,
      80,
      81,
      83,
      84,
      85,
      86,
      87,
      88,
      89,
      90,
      91,
      92,
      93,
      94,
      95,
      96,
      97,
      98,
      99,
      100,
      101,
      102,
      103,
      104,
      105,
      106,
      108,
      109,
      110,
      111,
      112,
      113,
      114,
      118,
      119,
      120,
      121,
      122,
      123,
      124,
      125,
      128,
      129,
      130,
      131,
      132,
      133,
      134,
      135,
      137,
      138,
      139,
      140,
      141,
      142,
      143,
      144,
      145,
      146,
      147,
      148,
      149,
      150,
      151,
      152,
      153,
      154,
      155,
      156,
      157,
      158,
      159,
      160,
      161,
      162,
      163,
      164,
      165,
      168,
      170,
      172,
      174,
      175,
      177,
      179,
      180
    ]
  },
  {
    "smgf": [
      1,
      2,
      8,
      9,
      10,
      13,
      14,
      15,
      16,
      17
    ],
    "pmgf": [
      20,
      21,
      23,
      25,
      28,
      39
    ],
    "mmgf": [
      45,
      46,
      47,
      48,
      49,
      50,
      51,
      52,
      53,
      54,
      55,
      56,
      57,
      59,
      60,
      61,
      62,
      63,
      64,
      65,
      67,
      68,
      69,
      70,
      71,
      73,
      75,
      80,
      81,
      82,
      83,
      84,
      85,
      86,
      87,
      88,
      89,
      93,
      94,
      95,
      96,
      97,
      98,
      99,
      100,
      101,
      102,
      105,
      106,
      107,
      108,
      109,
      110,
      111,
      112,
      113,
      114,
      116,
      117,
      118,
      119,
      120,
      121,
      122,
      123,
      124,
      125,
      126,
      127,
      128,
      129,
      130,
      131,
      132,
      133,
      134,
      135,
      136,
      137,
      138,
      139,
      140,
      141,
      142,
      143,
      144,
      145,
      146,
      147,
      148,
      150,
      152,
      153,
      154,
      156,
      157,
      158,
      159,
      161,
      162,
      163,
      164,
      165,
      166,
      167,
      168,
      169,
      170,
      171,
      172,
      173,
      174,
      175,
      176,
      177,
      179,
      180
    ]
  },
  {
    "smgf": [
      12,
      13,
      14,
      15,
      17
    ],
    "pmgf": [
      18,
      19,
      20,
      21,
      28,
      30,
      33,
      35,
      36,
      43
    ],
    "mmgf": [
      55,
      56,
      57,
      58,
      59,
      60,
      70,
      71,
      72,
      73,
      74,
      75,
      84,
      85,
      86,
      87,
      88,
      89,
      97,
      98,
      99,
      100,
      101,
      102,
      109,
      110,
      111,
      112,
      113,
      114,
      120,
      121,
      122,
      123,
      124,
      125,
      130,
      131,
      132,
      133,
      134,
      135,
      139,
      140,
      141,
      142,
      143,
      144,
      147,
      148,
      149,
      150,
      151,
      152,
      154,
      155,
      156,
      157,
      158,
      159,
      160,
      161,
      162,
      163,
      164,
      165,
      166,
      167,
      168,
      169,
      170,
      171,
      172,
      173,
      174,
      175,
      176,
      177,
      178,
      179,
      180
    ]
  },
  {
    "smgf": [
      1,
      3,
      4,
      9,
      10,
      13,
      15,
      16,
      17
    ],
    "pmgf": [
      19,
      24,
      29,
      37,
      41
    ],
    "mmgf": [
      45,
      46,
      47,
      48,
      49,
      50,
      51,
      52,
      53,
      54,
      55,
      56,
      57,
      58,
      59,
      60,
      61,
      67,
      68,
      69,
      70,
      71,
      72,
      73,
      74,
      75,
      81,
      82,
      83,
      84,
      85,
      86,
      87,
      88,
      89,
      90,
      91,
      92,
      93,
      95,
      96,
      97,
      100,
      102,
      106,
      107,
      108,
      109,
      110,
      111,
      112,
      113,
      114,
      117,
      118,
      119,
      120,
      121,
      122,
      123,
      124,
      125,
      127,
      128,
      129,
      130,
      131,
      132,
      133,
      134,
      135,
      136,
      137,
      138,
      139,
      140,
      141,
      142,
      143,
      144,
      145,
      146,
      147,
      148,
      149,
      150,
      151,
      152,
      153,
      154,
      157,
      159,
      161,
      162,
      163,
      164,
      166,
      167,
      168,
      169,
      171,
      172,
      173,
      175,
      177,
      179,
      180
    ]
  },
  {
    "smgf": [
      2,
      3,
      4,
      5,
      6,
      7,
      10,
      11,
      12,
      13,
      14
    ],
    "pmgf": [
      18,
      32,
      34,
      42,
      43,
      44
    ],
    "mmgf": [
      45,
      46,
      47,
      48,
      49,
      50,
      51,
      52,
      53,
      55,
      56,
      57,
      58,
      59,
      60,
      61,
      62,
      63,
      64,
      65,
      66,
      67,
      68,
      70,
      71,
      72,
      73,
      74,
      75,
      77,
      79,
      80,
      81,
      83,
      85,
      86,
      87,
      88,
      89,
      90,
      91,
      92,
      93,
      94,
      95,
      96,
      97,
      98,
      99,
      100,
      101,
      102,
      104,
      105,
      106,
      108,
      110,
      111,
      112,
      113,
      114,
      118,
      119,
      120,
      122,
      123,
      124,
      125,
      126,
      127,
      129,
      131,
      132,
      133,
      134,
      135,
      137,
      138,
      139,
      141,
      142,
      143,
      144,
      145,
      146,
      147,
      149,
      150,
      151,
      152,
      153,
      154,
      156,
      157,
      158,
      159,
      161,
      162,
      163,
      164,
      165,
      166,
      167,
      168,
      169,
      170,
      171,
      172,
      173,
      174,
      175,
      176,
      177
    ]
  },
  {
    "smgf": [
      1,
      2,
      11,
      13,
      15,
      17
    ],
    "pmgf": [
      20,
      21,
      23,
      31,
      33,
      35,
      38,
      41,
      43
    ],
    "mmgf": [
      45,
      46,
      47,
      48,
      49,
      50,
      51,
      52,
      53,
      54,
      55,
      56,
      57,
      58,
      59,
      61,
      62,
      63,
      64,
      65,
      66,
      67,
      68,
      71,
      72,
      73,
      74,
      75,
      83,
      84,
      85,
      86,
      87,
      88,
      89,
      96,
      97,
      98,
      99,
      100,
      101,
      102,
      108,
      109,
      110,
      111,
      112,
      113,
      114,
      119,
      120,
      121,
      122,
      123,
      124,
      125,
      129,
      130,
      131,
      132,
      133,
      134,
      135,
      138,
      139,
      140,
      141,
      142,
      143,
      144,
      146,
      147,
      148,
      149,
      150,
      151,
      152,
      153,
      154,
      155,
      156,
      157,
      158,
      159,
      160,
      161,
      162,
      163,
      164,
      165,
      166,
      167,
      168,
      169,
      170,
      171,
      172,
      173,
      174,
      175,
      176,
      177,
      178,
      179,
      180
    ]
  }
]

print(len(table))

mmgfs = [x["mmgf"] for x in table]

print(len(mmgfs))

set_mmgf = set()

all_sets = list(map(lambda x: set(x), mmgfs))

list(map(lambda x: set_mmgf.update(x), all_sets))


# set_mmgf.update(all_sets[14])
# set_mmgf.update(all_sets[11])


print(set_mmgf)

print(min(set_mmgf))

print(max(set_mmgf))

print(len(set_mmgf))