from from_xps_to_json import (
    parse_attendance_report,
    extract_session_and_date,
    extract_attendance,
)


def test_parse_attendance_report():
    text = """ 
    Câmara Municipal de Ferira de Santana
     
    Relatório de Presenças por Reunião
    Reunião : 1ª SESSÃO ORDINÁRIA    Dia : 01/02/2021
    ___________________________________________________________________________________________________
    Nº Nome Parlamentar               Partido 
    01 CORREIA ZEZITO                 PATRI   
    02 EDVALDO LIMA                   MDB     
    03 ELI RIBEIRO                    REP     
    04 EMERSON MINHO                  DC      
    05 EREMITA MOTA                   PSDB    
    06 FERNANDO TORRES                PSD     
    07 GALEGUINHO SPA                 PSB     
    08 GERUSA SAMPAIO                 DEM     
    09 JHONATAS MONTEIRO              PSOL    
    10 JOSÉ CARNEIRO                  MDB     
    11 JURANDY CARVALHO               PL      
    12 LÚ DE RONNY                    MDB     
    13 LUIZ DA FEIRA                  PROS    
    14 PAULÃO DO CALDEIRÃO            PSC     
    15 PEDRO AMÉRICO                  DEM     
    16 PEDRO CICERO                   CIDADAN 
    17 PR. VALDEMIR SANTOS            PV      
    18 PROFESSOR IVAMBERG             PT      
    19 RON DO POVO                    MDB     
    20 SILVIO DIAS                    PT      
    21 ZÉ CURUCA                      DEM     
    Ausências :
    Nome Parlamentar               Partido   
    Justificados :
    Nome Parlamentar               Partido    Texto                                             
    Totalização
    Presentes : 21      Ausentes : 0      Justificativas : 0
    _____________________________
    PRESIDENTE
    Yago Shamady
    09/02/2021 07:44
    1 
    """
    expected_attendance = {
        "agency": "Câmara Municipal de Ferira de Santana",
        "attendance": {
            "absent": [],
            "attending": [
                {"name": "CORREIA ZEZITO", "party": "PATRI", "text": ""},
                {"name": "EDVALDO LIMA", "party": "MDB", "text": ""},
                {"name": "ELI RIBEIRO", "party": "REP", "text": ""},
                {"name": "EMERSON MINHO", "party": "DC", "text": ""},
                {"name": "EREMITA MOTA", "party": "PSDB", "text": ""},
                {"name": "FERNANDO TORRES", "party": "PSD", "text": ""},
                {"name": "GALEGUINHO SPA", "party": "PSB", "text": ""},
                {"name": "GERUSA SAMPAIO", "party": "DEM", "text": ""},
                {"name": "JHONATAS MONTEIRO", "party": "PSOL", "text": ""},
                {"name": "JOSÉ CARNEIRO", "party": "MDB", "text": ""},
                {"name": "JURANDY CARVALHO", "party": "PL", "text": ""},
                {"name": "LÚ DE RONNY", "party": "MDB", "text": ""},
                {"name": "LUIZ DA FEIRA", "party": "PROS", "text": ""},
                {"name": "PAULÃO DO CALDEIRÃO", "party": "PSC", "text": ""},
                {"name": "PEDRO AMÉRICO", "party": "DEM", "text": ""},
                {"name": "PEDRO CICERO", "party": "CIDADAN", "text": ""},
                {"name": "PR. VALDEMIR SANTOS", "party": "PV", "text": ""},
                {"name": "PROFESSOR IVAMBERG", "party": "PT", "text": ""},
                {"name": "RON DO POVO", "party": "MDB", "text": ""},
                {"name": "SILVIO DIAS", "party": "PT", "text": ""},
                {"name": "ZÉ CURUCA", "party": "DEM", "text": ""},
            ],
            "justified": [],
            "report_from_text": {"absent": "0", "attending": "21", "justified": "0"},
        },
        "date": "01/02/2021",
        "report": "Relatório de Presenças por Reunião",
        "report_generated_at": "09/02/2021 07:44",
        "report_generated_by": "Yago Shamady",
        "session": "1ª SESSÃO ORDINÁRIA",
    }
    assert parse_attendance_report(text) == expected_attendance


def test_extract_session_and_date():
    line = "Reunião : 1ª SESSÃO ORDINÁRIA    Dia : 01/02/2021"
    expected_session = "1ª SESSÃO ORDINÁRIA"
    expected_date = "01/02/2021"
    assert extract_session_and_date(line) == (expected_session, expected_date)


def test_extract_attendance():
    lines = [
        "___",
        "Nº Nome Parlamentar               Partido",
        "01 CORREIA ZEZITO                 PATRI",
        "02 EDVALDO LIMA                   MDB",
        "03 ELI RIBEIRO                    REP",
        "Ausências :",
        "Nome Parlamentar               Partido   ",
        "RON DO POVO                    MDB",
        "Justificados :",
        "Nome Parlamentar               Partido    Texto",
        "PEDRO CICERO                   CIDADAN          LICENÇA",
        "Totalização",
        "Presentes : 21      Ausentes : 1      Justificativas : 1",
        "___",
    ]
    expected_attendance = {
        "attending": [
            {"name": "CORREIA ZEZITO", "party": "PATRI", "text": ""},
            {"name": "EDVALDO LIMA", "party": "MDB", "text": ""},
            {"name": "ELI RIBEIRO", "party": "REP", "text": ""},
        ],
        "absent": [
            {"name": "RON DO POVO", "party": "MDB", "text": ""},
        ],
        "justified": [
            {"name": "PEDRO CICERO", "party": "CIDADAN", "text": "LICENÇA"},
        ],
        "report_from_text": {
            "attending": "21",
            "absent": "1",
            "justified": "1",
        },
    }
    attendance = extract_attendance(lines)
    assert attendance == expected_attendance


def test_extract_attendance_with_rearrangement():
    lines = [
        "___________________________________________________________________________________________________",
        "Nº Nome Parlamentar               Partido ",
        "01 ANTONIO CARLOS ATAÍDE          DEM     ",
        "02 CADMIEL PEREIRA                DEM     ",
        "03 EDVALDO LIMA                   MDB     ",
        "04 EREMITA MOTA                   PSDB    ",
        "05 FABIANO DA VAN                 MDB     ",
        "06 GERUSA SAMPAIO                 DEM     ",
        "07 GILMAR AMORIM                  MDB     ",
        "08 ISAÍAS DE DIOGO                MDB     ",
        "09 JOÃO BILILIU                   PSD     ",
        "10 JOSÉ CARNEIRO                  MDB     ",
        "11 LUIZ DA FEIRA                  PROS    ",
        "12 LULINHA                        DEM     ",
        "13 MARCOS LIMA                    DEM     ",
        "14 NEINHA                         DEM     ",
        "15 ROBERTO TOURINHO               PSB     ",
        "16 RON DO POVO                    MDB     ",
        "17 ZÉ FILÉ                        PSD     ",
        "      Recomposição de Quorum                             09:45:33 ",
        "Nº Nome Parlamentar               Partido ",
        "01 ANTONIO CARLOS ATAÍDE          DEM     ",
        "02 CADMIEL PEREIRA                DEM     ",
        "03 EDVALDO LIMA                   MDB     ",
        "04 EREMITA MOTA                   PSDB    ",
        "05 FABIANO DA VAN                 MDB     ",
        "06 GERUSA SAMPAIO                 DEM     ",
        "07 GILMAR AMORIM                  MDB     ",
        "08 ISAÍAS DE DIOGO                MDB     ",
        "09 JOÃO BILILIU                   PSD     ",
        "10 JOSÉ CARNEIRO                  MDB     ",
        "11 LUIZ DA FEIRA                  PROS    ",
        "12 LULINHA                        DEM     ",
        "13 MARCOS LIMA                    DEM     ",
        "14 NEINHA                         DEM     ",
        "15 ROBERTO TOURINHO               PSB     ",
        "16 RON DO POVO                    MDB     ",
        "17 ZÉ CURUCA                      DEM     ",
        "18 ZÉ FILÉ                        PSD     ",
        "Ausências :",
        "Nome Parlamentar               Partido   ",
        "ALBERTO NERY                   PT        ",
        "CÍNTIA MACHADO                 REP       ",
        "PR TOM                         PATRI     ",
        "Justificados :",
        "Nome Parlamentar               Partido    "
        "Texto                                             ",
        "ELI RIBEIRO                    REP        "
        "LICENCIADO                                        ",
        "JUSTINIANO FRANÇA              DEM        "
        "LICENCIADO                                        ",
        "PABLO ROBERTO                  DEM        "
        "LICENCIADO                                        ",
        "ROBECI DA VASSOURA             PHS        "
        "SUPLENTE                                          ",
        "RONNY                          PHS        "
        "FALECIMENTO                                       ",
        "SGT JOSAFÁ RAMOS               PATRI      "
        "SUPLENTE                                          ",
        "Totalização",
        "Presentes : 18      Ausentes : 3      Justificativas : 6",
        "Yago Shamady",
        "29/05/2020 12:11",
        "1",
        " ",
        "Câmara Municipal de Ferira de Santana",
        " ",
        "_____________________________",
    ]

    expected_attendance = {
        "absent": [
            {"name": "ALBERTO NERY", "party": "PT", "text": ""},
            {"name": "CÍNTIA MACHADO", "party": "REP", "text": ""},
            {"name": "PR TOM", "party": "PATRI", "text": ""},
        ],
        "attending": [
            {"name": "ANTONIO CARLOS ATAÍDE", "party": "DEM", "text": ""},
            {"name": "CADMIEL PEREIRA", "party": "DEM", "text": ""},
            {"name": "EDVALDO LIMA", "party": "MDB", "text": ""},
            {"name": "EREMITA MOTA", "party": "PSDB", "text": ""},
            {"name": "FABIANO DA VAN", "party": "MDB", "text": ""},
            {"name": "GERUSA SAMPAIO", "party": "DEM", "text": ""},
            {"name": "GILMAR AMORIM", "party": "MDB", "text": ""},
            {"name": "ISAÍAS DE DIOGO", "party": "MDB", "text": ""},
            {"name": "JOÃO BILILIU", "party": "PSD", "text": ""},
            {"name": "JOSÉ CARNEIRO", "party": "MDB", "text": ""},
            {"name": "LUIZ DA FEIRA", "party": "PROS", "text": ""},
            {"name": "LULINHA", "party": "DEM", "text": ""},
            {"name": "MARCOS LIMA", "party": "DEM", "text": ""},
            {"name": "NEINHA", "party": "DEM", "text": ""},
            {"name": "ROBERTO TOURINHO", "party": "PSB", "text": ""},
            {"name": "RON DO POVO", "party": "MDB", "text": ""},
            {"name": "ZÉ FILÉ", "party": "PSD", "text": ""},
        ],
        "justified": [
            {"name": "ELI RIBEIRO", "party": "REP", "text": "LICENCIADO"},
            {"name": "JUSTINIANO FRANÇA", "party": "DEM", "text": "LICENCIADO"},
            {"name": "PABLO ROBERTO", "party": "DEM", "text": "LICENCIADO"},
            {"name": "ROBECI DA VASSOURA", "party": "PHS", "text": "SUPLENTE"},
            {"name": "RONNY", "party": "PHS", "text": "FALECIMENTO"},
            {"name": "SGT JOSAFÁ RAMOS", "party": "PATRI", "text": "SUPLENTE"},
        ],
        "rearrangement": [
            {"name": "ANTONIO CARLOS ATAÍDE", "party": "DEM", "text": ""},
            {"name": "CADMIEL PEREIRA", "party": "DEM", "text": ""},
            {"name": "EDVALDO LIMA", "party": "MDB", "text": ""},
            {"name": "EREMITA MOTA", "party": "PSDB", "text": ""},
            {"name": "FABIANO DA VAN", "party": "MDB", "text": ""},
            {"name": "GERUSA SAMPAIO", "party": "DEM", "text": ""},
            {"name": "GILMAR AMORIM", "party": "MDB", "text": ""},
            {"name": "ISAÍAS DE DIOGO", "party": "MDB", "text": ""},
            {"name": "JOÃO BILILIU", "party": "PSD", "text": ""},
            {"name": "JOSÉ CARNEIRO", "party": "MDB", "text": ""},
            {"name": "LUIZ DA FEIRA", "party": "PROS", "text": ""},
            {"name": "LULINHA", "party": "DEM", "text": ""},
            {"name": "MARCOS LIMA", "party": "DEM", "text": ""},
            {"name": "NEINHA", "party": "DEM", "text": ""},
            {"name": "ROBERTO TOURINHO", "party": "PSB", "text": ""},
            {"name": "RON DO POVO", "party": "MDB", "text": ""},
            {"name": "ZÉ CURUCA", "party": "DEM", "text": ""},
            {"name": "ZÉ FILÉ", "party": "PSD", "text": ""},
        ],
        "report_from_text": {"absent": "3", "attending": "18", "justified": "6"},
    }
    attendance = extract_attendance(lines)
    assert attendance == expected_attendance


def test_extract_sentences_from_justification():
    lines = [
        "___________________________________________________________________________________________________",
        "Nº Nome Parlamentar               Partido ",
        "01 ALBERTO NERY                   PT      ",
        "02 CADMIEL PEREIRA                DEM     ",
        "03 EDVALDO LIMA                   MDB     ",
        "04 ELI RIBEIRO                    REP     ",
        "05 FABIANO DA VAN                 MDB     ",
        "06 GERUSA SAMPAIO                 DEM     ",
        "07 GILMAR AMORIM                  MDB     ",
        "08 ISAÍAS DE DIOGO                MDB     ",
        "09 JOSÉ CARNEIRO                  MDB     ",
        "10 LUIZ DA FEIRA                  PROS    ",
        "11 LULINHA                        DEM     ",
        "12 MARCOS LIMA                    DEM     ",
        "13 NEINHA                         DEM     ",
        "14 ROBERTO TOURINHO               PSB     ",
        "15 RON DO POVO                    MDB     ",
        "16 SGT JOSAFÁ RAMOS               PATRI   ",
        "17 ZÉ CURUCA                      DEM     ",
        "18 ZÉ FILÉ                        PSD     ",
        "Ausências :",
        "Nome Parlamentar               Partido   ",
        "Justificados :",
        "Nome Parlamentar               Partido    Texto                                             ",
        "ANTONIO CARLOS ATAÍDE          DEM        PORTARIA Nº 276                                   ",
        "CÍNTIA MACHADO                 REP        SUPLENTE                                          ",
        "EREMITA MOTA                   PSDB       PORTARIA Nº 276                                   ",
        "JOÃO BILILIU                   PSD        PORTARIA Nº 276                                   ",
        "JUSTINIANO FRANÇA              DEM        LICENCIADO                                        ",
        "PABLO ROBERTO                  DEM        LICENCIADO                                        ",
        "PR TOM                         PATRI      RENÚNCIA                                          ",
        "ROBECI DA VASSOURA             PHS        SUPLENTE                                          ",
        "RONNY                          PHS        FALECIMENTO                                       ",
        "Totalização",
        "Presentes : 18      Ausentes : 0      Justificativas : 9",
        "_____________________________",
    ]

    expected_attendance = {
        "attending": [
            {"name": "ALBERTO NERY", "party": "PT", "text": ""},
            {"name": "CADMIEL PEREIRA", "party": "DEM", "text": ""},
            {"name": "EDVALDO LIMA", "party": "MDB", "text": ""},
            {"name": "ELI RIBEIRO", "party": "REP", "text": ""},
            {"name": "FABIANO DA VAN", "party": "MDB", "text": ""},
            {"name": "GERUSA SAMPAIO", "party": "DEM", "text": ""},
            {"name": "GILMAR AMORIM", "party": "MDB", "text": ""},
            {"name": "ISAÍAS DE DIOGO", "party": "MDB", "text": ""},
            {"name": "JOSÉ CARNEIRO", "party": "MDB", "text": ""},
            {"name": "LUIZ DA FEIRA", "party": "PROS", "text": ""},
            {"name": "LULINHA", "party": "DEM", "text": ""},
            {"name": "MARCOS LIMA", "party": "DEM", "text": ""},
            {"name": "NEINHA", "party": "DEM", "text": ""},
            {"name": "ROBERTO TOURINHO", "party": "PSB", "text": ""},
            {"name": "RON DO POVO", "party": "MDB", "text": ""},
            {"name": "SGT JOSAFÁ RAMOS", "party": "PATRI", "text": ""},
            {"name": "ZÉ CURUCA", "party": "DEM", "text": ""},
            {"name": "ZÉ FILÉ", "party": "PSD", "text": ""},
        ],
        "absent": [],
        "justified": [
            {
                "name": "ANTONIO CARLOS ATAÍDE",
                "party": "DEM",
                "text": "PORTARIA Nº 276",
            },
            {"name": "CÍNTIA MACHADO", "party": "REP", "text": "SUPLENTE"},
            {"name": "EREMITA MOTA", "party": "PSDB", "text": "PORTARIA Nº 276"},
            {"name": "JOÃO BILILIU", "party": "PSD", "text": "PORTARIA Nº 276"},
            {"name": "JUSTINIANO FRANÇA", "party": "DEM", "text": "LICENCIADO"},
            {"name": "PABLO ROBERTO", "party": "DEM", "text": "LICENCIADO"},
            {"name": "PR TOM", "party": "PATRI", "text": "RENÚNCIA"},
            {"name": "ROBECI DA VASSOURA", "party": "PHS", "text": "SUPLENTE"},
            {"name": "RONNY", "party": "PHS", "text": "FALECIMENTO"},
        ],
        "report_from_text": {"attending": "18", "absent": "0", "justified": "9"},
    }
    attendance = extract_attendance(lines)
    assert attendance == expected_attendance
