from from_xps_to_json import parse_attendance_report, extract_session_and_date


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
        "report": "Relatório de Presenças por Reunião",
        "session": "1ª SESSÃO ORDINÁRIA",
        "date": "01/02/2021",
        "attendance": {
            "city_councils": {
                "attending": [
                    {"name": "", "party": ""},
                    {"name": "", "party": ""},
                    {"name": "", "party": ""},
                ],
                "absent": [
                    {"name": "", "party": ""},
                    {"name": "", "party": ""},
                    {"name": "", "party": ""},
                ],
                "justified": [
                    {"name": "", "party": ""},
                    {"name": "", "party": ""},
                    {"name": "", "party": ""},
                ],
            },
            "report_from_text": {
                "attending": "21",
                "absent": "0",
                "justified": "0",
            }
        },
        "president": "Yago Shamady",
        "report_generated_at": "09/02/2021 07:44"
    }
    assert parse_attendance_report(text) == expected_attendance


def test_extract_session_and_date():
    line = "Reunião : 1ª SESSÃO ORDINÁRIA    Dia : 01/02/2021"
    expected_session = "1ª SESSÃO ORDINÁRIA"
    expected_date = "01/02/2021"
    assert extract_session_and_date(line) == (expected_session, expected_date)
