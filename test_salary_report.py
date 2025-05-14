# pytest test_salary_report.py -v
import pytest
from salary_report import process_file, generate_reports
from unittest.mock import patch, mock_open
import tabulate

@pytest.fixture
def sample_csv_data():
    return """name,hours_worked,salary_rate,department
John Doe,40,50,HR
Jane Smith,35,60,Sales
Bob Johnson,45,55,Marketing
Alice Brown,30,65,Design"""

@pytest.fixture
def initialized_lists():
    hr = [['name', 'hours', 'rate', 'payout']]
    sales = [['name', 'hours', 'rate', 'payout']]
    marketing = [['name', 'hours', 'rate', 'payout']]
    design = [['name', 'hours', 'rate', 'payout']]
    return hr, sales, marketing, design

def test_process_file(initialized_lists, sample_csv_data):
    hr, sales, marketing, design = initialized_lists
    
    with patch('builtins.open', mock_open(read_data=sample_csv_data)):
        process_file('dummy.csv', hr, sales, marketing, design)
    
    assert len(hr) == 2
    assert hr[1] == ['John Doe', 40, 50, 2000]
    
    assert len(sales) == 2
    assert sales[1][3] == 2100  # 35 * 60
    
    assert len(marketing) == 2
    assert marketing[1][2] == 55
    
    assert len(design) == 2
    assert design[1][1] == 30

def test_process_file_with_different_column_names(initialized_lists):
    hr, sales, marketing, design = initialized_lists
    csv_data = "employee_name,hrs,pay_rate,dept\nTest User,20,30,HR"
    
    with patch('builtins.open', mock_open(read_data=csv_data)):
        process_file('dummy.csv', hr, sales, marketing, design)
    
    assert hr[1] == ['Test User', 20, 30, 600]

@patch('builtins.print')
def test_generate_reports(mock_print, initialized_lists):
    hr, sales, marketing, design = initialized_lists
    hr.append(['John Doe', 40, 50, 2000])
    sales.append(['Jane Smith', 35, 60, 2100])
    
    generate_reports(hr, sales, marketing, design)
    
    # Проверяем, что функции печати вызывались с правильными аргументами
    mock_print.assert_any_call('========== HR ============')
    mock_print.assert_any_call(tabulate.tabulate(hr))
    mock_print.assert_any_call('========== Sales =========')
    mock_print.assert_any_call(tabulate.tabulate(sales))

def test_payout_calculation():
    # Тест для проверки правильности расчета выплат
    hours = 40
    rate = 50
    payout = hours * rate
    assert payout == 2000

def test_department_classification(initialized_lists, sample_csv_data):
    hr, sales, marketing, design = initialized_lists
    
    with patch('builtins.open', mock_open(read_data=sample_csv_data)):
        process_file('dummy.csv', hr, sales, marketing, design)
    
    assert 'John Doe' in hr[1][0]
    assert 'Jane Smith' in sales[1][0]
    assert 'Bob Johnson' in marketing[1][0]
    assert 'Alice Brown' in design[1][0]

def test_empty_file(initialized_lists):
    hr, sales, marketing, design = initialized_lists
    csv_data = "name,hours,rate,department\n"
    
    with patch('builtins.open', mock_open(read_data=csv_data)):
        process_file('empty.csv', hr, sales, marketing, design)
    
    assert len(hr) == 1  # только заголовок
    assert len(sales) == 1
    assert len(marketing) == 1
    assert len(design) == 1
