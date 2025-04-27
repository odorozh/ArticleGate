INSERT INTO article (doi, title, posting_date) VALUES
(
    "10.1101/2025.04.16.649184",
    "Genetic mapping of resistance: A QTL and associated polymorphism conferring resistance to alpha-cypermethrin in Anopheles funestus",
    "2025-04-22"
),
(
    "10.1101/2023.05.16.540925",
    "The contribution of an X chromosome QTL to non-Mendelian inheritance and unequal chromosomal segregation in A. freiburgense",
    "2023-08-26"
),
(
    "10.1101/2023.08.25.554687",
    "Overexpression and nonsynonymous mutations of UDP-glycosyltransferases potentially associated with pyrethroid resistance in Anopheles funestus",
    "2023-08-25"
),
(
    "10.1101/2022.03.21.485146",
    "Molecular drivers of insecticide resistance in the Sahelo-Sudanian populations of a major malaria vector Anopheles coluzzii",
    "2023-02-01"
),
(
    "10.1101/2021.11.25.470000",
    "Gene conversion explains elevated diversity in the immunity modulating APL1 gene of the malaria vector Anopheles funestus",
    "2021-11-25"
),
(
    "10.1101/2020.05.05.078600",
    "A 6.5kb intergenic structural variation enhances P450-mediated resistance to pyrethroids in malaria vectors lowering bed net efficacy",
    "2020-05-07"
);

-- ================================================================

INSERT INTO organisation (id, title, location) VALUES
(
    0,
    "Liverpool School of Tropical Medicine",
    "Liverpool, UK"
),
(
    1,
    "Centre for Research in Infectious Diseases",
    "Yaoundé, Cameroon"
),
(
    2,
    "Syngenta Crop Protection",
    "Basel, Switzerland"
),
(
    3,
    "Scotland's Rural College",
    "Scotland, UK"
),
(
    4,
    "University of Warwick",
    "Coventry, UK"
),
(
    5,
    "Seoul National University",
    "Seoul, Republic of Korea"
),
(
    6,
    "Mississippi State University",
    "Mississippi, USA"
),
(
    7,
    "Liverpool John Moores University",
    "Liverpool, UK"
),
(
    8,
    "Bayero University",
    "PMB 3011, Kano, Nigeria"
),
(
    9,
    "Brock University",
    "St. Catharines, Ontario, Canada"
),
(
    10,
    "University of Buea",
    "Buea, Cameroon"
);

-- ================================================================

INSERT INTO author (id, name, affiliation_org_id) VALUES
(
    0,
    "Talal AL-Yazeedi",
    0
),
(
    1,
    "Grâce Djuifo",
    1
),
(
    2,
    "Leon Mugenzi",
    2
),
(
    3,
    "Abdullahi Muhammad",
    0
),
(
    4,
    "Jack Hearn",
    3
),
(
    5,
    "Charles S. Wondji",
    0
),
(
    6,
    "Sally Adams",
    4
),
(
    7,
    "Sophie Tandonnet",
    4
),
(
    8,
    "Anisa Turner",
    4
),
(
    9,
    "Jun Kim",
    5
),
(
    10,
    "Junho Lee",
    5
),
(
    11,
    "Andre Pires-daSilva",
    4
),
(
    12,
    "Helen Irving",
    0
),
(
    13,
    "Seung-Joon Ahn",
    6
),
(
    14,
    "Sulaiman S. Ibrahim",
    0
),
(
    15,
    "Gareth D. Weedall",
    7
),
(
    16,
    "Sanjay C. Nagi",
    0
),
(
    17,
    "Muhammad M. Mukhtar",
    8
),
(
    18,
    "Amen N. Fadel",
    1
),
(
    19,
    "Leon J. Mugenzi",
    1
),
(
    20,
    "Edward I. Patterson",
    9
),
(
    21,
    "Jacob M. Riveron",
    0
),
(
    22,
    "Benjamin D. Menze",
    0
),
(
    23,
    "Magellan Tchouakui",
    1
),
(
    24,
    "Murielle J. Wondji",
    0
),
(
    25,
    "Micareme Tchoupo",
    1
),
(
    26,
    "Fidelis Cho-Ngwa",
    10
);

-- ================================================================

-- Info about DOI 10.1101/2025.04.16.649184
INSERT INTO article_to_author (doi, author_id, place) VALUES
(
    "10.1101/2025.04.16.649184",
    0,
    1
),
(
    "10.1101/2025.04.16.649184",
    1,
    2
),
(
    "10.1101/2025.04.16.649184",
    2,
    3
),
(
    "10.1101/2025.04.16.649184",
    3,
    4
),
(
    "10.1101/2025.04.16.649184",
    4,
    5
),
(
    "10.1101/2025.04.16.649184",
    5,
    6
);

-- Info about DOI 10.1101/2023.05.16.540925
INSERT INTO article_to_author (doi, author_id, place) VALUES
(
    "10.1101/2023.05.16.540925",
    0,
    1
),
(
    "10.1101/2023.05.16.540925",
    6,
    2
),
(
    "10.1101/2023.05.16.540925",
    7,
    3
),
(
    "10.1101/2023.05.16.540925",
    8,
    4
),
(
    "10.1101/2023.05.16.540925",
    9,
    5
),
(
    "10.1101/2023.05.16.540925",
    10,
    6
),
(
    "10.1101/2023.05.16.540925",
    11,
    6
);

-- Info about DOI 10.1101/2023.08.25.554687
INSERT INTO article_to_author (doi, author_id, place) VALUES
(
    "10.1101/2023.08.25.554687",
    0,
    1
),
(
    "10.1101/2023.08.25.554687",
    3,
    2
),
(
    "10.1101/2023.08.25.554687",
    12,
    3
),
(
    "10.1101/2023.08.25.554687",
    13,
    4
),
(
    "10.1101/2023.08.25.554687",
    4,
    5
),
(
    "10.1101/2023.08.25.554687",
    5,
    6
);

-- Info about DOI 10.1101/2022.03.21.485146
INSERT INTO article_to_author (doi, author_id, place) VALUES
(
    "10.1101/2022.03.21.485146",
    14,
    1
),
(
    "10.1101/2022.03.21.485146",
    3,
    2
),
(
    "10.1101/2022.03.21.485146",
    4,
    3
),
(
    "10.1101/2022.03.21.485146",
    15,
    4
),
(
    "10.1101/2022.03.21.485146",
    16,
    5
),
(
    "10.1101/2022.03.21.485146",
    17,
    6
),
(
    "10.1101/2022.03.21.485146",
    18,
    7
),
(
    "10.1101/2022.03.21.485146",
    19,
    8
),
(
    "10.1101/2022.03.21.485146",
    20,
    9
),
(
    "10.1101/2022.03.21.485146",
    5,
    10
);

-- Info about DOI 10.1101/2021.11.25.470000
INSERT INTO article_to_author (doi, author_id, place) VALUES
(
    "10.1101/2021.11.25.470000",
    4,
    1
),
(
    "10.1101/2021.11.25.470000",
    21,
    2
),
(
    "10.1101/2021.11.25.470000",
    12,
    3
),
(
    "10.1101/2021.11.25.470000",
    15,
    4
),
(
    "10.1101/2021.11.25.470000",
    5,
    5
);

-- Info about DOi 10.1101/2020.05.05.078600
INSERT INTO article_to_author (doi, author_id, place) VALUES
(
    "10.1101/2020.05.05.078600",
    19,
    1
),
(
    "10.1101/2020.05.05.078600",
    22,
    2
),
(
    "10.1101/2020.05.05.078600",
    23,
    3
),
(
    "10.1101/2020.05.05.078600",
    24,
    4
),
(
    "10.1101/2020.05.05.078600",
    12,
    5
),
(
    "10.1101/2020.05.05.078600",
    25,
    6
),
(
    "10.1101/2020.05.05.078600",
    4,
    7
),
(
    "10.1101/2020.05.05.078600",
    15,
    8
),
(
    "10.1101/2020.05.05.078600",
    21,
    9
),
(
    "10.1101/2020.05.05.078600",
    26,
    10
),
(
    "10.1101/2020.05.05.078600",
    5,
    11
);
