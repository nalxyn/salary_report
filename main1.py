import argparse
import tabulate

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', type=str, help='Salary report')
    return parser.parse_args()

def process_file(file_path, hr, sales, marketing, design):
    with open(file_path.strip()) as f:
        data = f.readlines()
    
    title = data[0].split(',')
    salary, name, hours = None, None, None
    
    for x in title:
        x_lower = x.lower()
        if 'salary' in x_lower or 'rate' in x_lower:
            salary = title.index(x)
        if 'name' in x_lower:
            name = title.index(x)
        if 'hours' in x_lower:
            hours = title.index(x)

    for line in data[1:]:
        y = line.split(',')
        info = [
            y[name].strip(),
            int(y[hours].strip()),
            int(y[salary].strip()),
            int(y[hours].strip()) * int(y[salary].strip())
        ]
        
        if 'Design' in line:
            design.append(info)
        elif 'Marketing' in line:
            marketing.append(info)
        elif 'Sales' in line:
            sales.append(info)
        elif 'HR' in line:
            hr.append(info)

def generate_reports(hr, sales, marketing, design):
    print('========== HR ============')
    print(tabulate.tabulate(hr))
    print('========== Sales =========')
    print(tabulate.tabulate(sales))
    print('========== Marketing =====')
    print(tabulate.tabulate(marketing))
    print('========== Design ========')
    print(tabulate.tabulate(design))

def main():
    hr = [['name', 'hours', 'rate', 'payout']]
    sales = [['name', 'hours', 'rate', 'payout']]
    marketing = [['name', 'hours', 'rate', 'payout']]
    design = [['name', 'hours', 'rate', 'payout']]
    
    args = parse_arguments()
    files = args.report.split(' ')
    
    for file in files:
        process_file(file, hr, sales, marketing, design)
    
    generate_reports(hr, sales, marketing, design)

if __name__ == "__main__":
    main()
