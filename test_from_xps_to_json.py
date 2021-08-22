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
                {"name": "CORREIA ZEZITO", "party": "PATRI"},
                {"name": "EDVALDO LIMA", "party": "MDB"},
                {"name": "ELI RIBEIRO", "party": "REP"},
                {"name": "EMERSON MINHO", "party": "DC"},
                {"name": "EREMITA MOTA", "party": "PSDB"},
                {"name": "FERNANDO TORRES", "party": "PSD"},
                {"name": "GALEGUINHO SPA", "party": "PSB"},
                {"name": "GERUSA SAMPAIO", "party": "DEM"},
                {"name": "JHONATAS MONTEIRO", "party": "PSOL"},
                {"name": "JOSÉ CARNEIRO", "party": "MDB"},
                {"name": "JURANDY CARVALHO", "party": "PL"},
                {"name": "LÚ DE RONNY", "party": "MDB"},
                {"name": "LUIZ DA FEIRA", "party": "PROS"},
                {"name": "PAULÃO DO CALDEIRÃO", "party": "PSC"},
                {"name": "PEDRO AMÉRICO", "party": "DEM"},
                {"name": "PEDRO CICERO", "party": "CIDADAN"},
                {"name": "PR. VALDEMIR SANTOS", "party": "PV"},
                {"name": "PROFESSOR IVAMBERG", "party": "PT"},
                {"name": "RON DO POVO", "party": "MDB"},
                {"name": "SILVIO DIAS", "party": "PT"},
                {"name": "ZÉ CURUCA", "party": "DEM"},
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
            {"name": "CORREIA ZEZITO", "party": "PATRI"},
            {"name": "EDVALDO LIMA", "party": "MDB"},
            {"name": "ELI RIBEIRO", "party": "REP"},
        ],
        "absent": [
            {"name": "RON DO POVO", "party": "MDB"},
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
            {"name": "ALBERTO NERY", "party": "PT"},
            {"name": "CÍNTIA MACHADO", "party": "REP"},
            {"name": "PR TOM", "party": "PATRI"},
        ],
        "attending": [
            {"name": "ANTONIO CARLOS ATAÍDE", "party": "DEM"},
            {"name": "CADMIEL PEREIRA", "party": "DEM"},
            {"name": "EDVALDO LIMA", "party": "MDB"},
            {"name": "EREMITA MOTA", "party": "PSDB"},
            {"name": "FABIANO DA VAN", "party": "MDB"},
            {"name": "GERUSA SAMPAIO", "party": "DEM"},
            {"name": "GILMAR AMORIM", "party": "MDB"},
            {"name": "ISAÍAS DE DIOGO", "party": "MDB"},
            {"name": "JOÃO BILILIU", "party": "PSD"},
            {"name": "JOSÉ CARNEIRO", "party": "MDB"},
            {"name": "LUIZ DA FEIRA", "party": "PROS"},
            {"name": "LULINHA", "party": "DEM"},
            {"name": "MARCOS LIMA", "party": "DEM"},
            {"name": "NEINHA", "party": "DEM"},
            {"name": "ROBERTO TOURINHO", "party": "PSB"},
            {"name": "RON DO POVO", "party": "MDB"},
            {"name": "ZÉ FILÉ", "party": "PSD"},
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
            {"name": "ANTONIO CARLOS ATAÍDE", "party": "DEM"},
            {"name": "CADMIEL PEREIRA", "party": "DEM"},
            {"name": "EDVALDO LIMA", "party": "MDB"},
            {"name": "EREMITA MOTA", "party": "PSDB"},
            {"name": "FABIANO DA VAN", "party": "MDB"},
            {"name": "GERUSA SAMPAIO", "party": "DEM"},
            {"name": "GILMAR AMORIM", "party": "MDB"},
            {"name": "ISAÍAS DE DIOGO", "party": "MDB"},
            {"name": "JOÃO BILILIU", "party": "PSD"},
            {"name": "JOSÉ CARNEIRO", "party": "MDB"},
            {"name": "LUIZ DA FEIRA", "party": "PROS"},
            {"name": "LULINHA", "party": "DEM"},
            {"name": "MARCOS LIMA", "party": "DEM"},
            {"name": "NEINHA", "party": "DEM"},
            {"name": "ROBERTO TOURINHO", "party": "PSB"},
            {"name": "RON DO POVO", "party": "MDB"},
            {"name": "ZÉ CURUCA", "party": "DEM"},
            {"name": "ZÉ FILÉ", "party": "PSD"},
        ],
        "report_from_text": {"absent": "3", "attending": "18", "justified": "6"},
    }
    attendance = extract_attendance(lines)
    assert attendance == expected_attendance
