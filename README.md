# ArticleGate

Проект по курсу "Программирование на Python" Цифровой Кафедры МФТИ

## Общее описание

WEB-приложение для организации сведений о научных публикациях.

## Структура данных

Основным сущностями в базе данных явлются таблицы author, article и organisation.

У каждого автора есть организация, с которой он аффилирован. У каждой статьи есть набор упорядоченных авторов.

Для связи статей с авторами используется таблица article_to_author. В этой таблице каждая строка хранит DOI статьи, идентификатор автора и номер его указания среди авторов рассматриваемой статьи.

![ArticleGate DB](imgs/ArticleGateDB.png "Схема базы данных")

## Стек технологий

+ Python3
+ FastAPI
+ SQLite3
+ SQLAlchemy
+ Pydentic
+ Pylint

## Citation

Для наполнения тестовой базы данных использованы данные некоторых научных публикаций с сайта [https://www.biorxiv.org/](bioRxiv).

Ниже приведён их исчерпывающий список:

1.  Genetic mapping of resistance: A QTL and associated polymorphism conferring resistance to alpha-cypermethrin in Anopheles funestus. Talal AL-Yazeedi, Grâce Djuifo, Leon Mugenzi, Abdullahi Muhammad, Jack Hearn, Charles S. Wondji
bioRxiv 2025.04.16.649184; doi: https://doi.org/10.1101/2025.04.16.649184

2.  A QTL influences sex ratios by controlling asymmetric organelle positioning during male spermatogenesis in Auanema freiburgense
Talal Al-Yazeedi, Sally Adams, Sophie Tandonnet, Anisa Turner, Jun Kim, Junho Lee, Andre Pires-daSilva
bioRxiv 2023.05.16.540925; doi: https://doi.org/10.1101/2023.05.16.540925 

3. Overexpression and nonsynonymous mutations of UDP-glycosyltransferases potentially associated with pyrethroid resistance in Anopheles funestus
Talal Al-Yazeedi, Abdullahi Muhammad, Helen Irving, Seung-Joon Ahn, Jack Hearn, Charles S. Wondji
bioRxiv 2023.08.25.554687; doi: https://doi.org/10.1101/2023.08.25.554687 

4.  Molecular drivers of insecticide resistance in the Sahelo-Sudanian populations of a major malaria vector Anopheles coluzzii
Sulaiman S. Ibrahim, Abdullahi Muhammad, Jack Hearn, Gareth D. Weedall, Sanjay C. Nagi, Muhammad M. Mukhtar, Amen N. Fadel, Leon J. Mugenzi, Edward I. Patterson, Helen Irving, Charles S. Wondji
bioRxiv 2022.03.21.485146; doi: https://doi.org/10.1101/2022.03.21.485146 

5.  Gene conversion explains elevated diversity in the immunity modulating APL1 gene of the malaria vector Anopheles funestus
Jack Hearn, Jacob M. Riveron, Helen Irving, Gareth D. Weedall, Charles S. Wondji
bioRxiv 2021.11.25.470000; doi: https://doi.org/10.1101/2021.11.25.470000 

6.  A 6.5kb intergenic structural variation enhances P450-mediated resistance to pyrethroids in malaria vectors lowering bed net efficacy
Leon M.J. Mugenzi, Benjamin D. Menze, Magellan Tchouakui, Murielle J. Wondji, Helen Irving, Micareme Tchoupo, Jack Hearn, Gareth D. Weedall, Jacob M. Riveron, Fidelis Cho-Ngwa, Charles S. Wondji
bioRxiv 2020.05.05.078600; doi: https://doi.org/10.1101/2020.05.05.078600 