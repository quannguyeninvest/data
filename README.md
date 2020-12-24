# Stocks

## Download Data
```bash
# VNX
EXCHANGE=VNX
npm run download -- --exchange=$EXCHANGE --type=BalanceSheet,IncomeStatement,DCashFlow,ICashFlow,Indicators --year=2015
npm run download -- --exchange=$EXCHANGE --type=BalanceSheet,IncomeStatement,DCashFlow,ICashFlow,Indicators --year=2020
for YEAR in {2015..2020}
do
npm run download -- --exchange=$EXCHANGE --type=BalanceSheetQuarter,IncomeStatementQuarter,DCashFlowQuarter,ICashFlowQuarter,IndicatorsQuarter --year=$YEAR
sleep 10
done

npm run download -- --exchange=$EXCHANGE --type=BalanceSheet,IncomeStatement,DCashFlow,ICashFlow,Indicators --update=1
npm run download -- --exchange=$EXCHANGE --type=BalanceSheetQuarter,IncomeStatementQuarter,DCashFlowQuarter,ICashFlowQuarter,IndicatorsQuarter --update=1

# SSL: NODE_TLS_REJECT_UNAUTHORIZED=0
# Prices
NODE_TLS_REJECT_UNAUTHORIZED=0 npm run download -- --exchange=VNX --type=Price,Events,Report
npm run download -- --exchange=VN30F --type=Prices
NODE_TLS_REJECT_UNAUTHORIZED=0 npm run download -- --exchange=VN30F --type=Price --symbols=gold,E1VFVN30
# Zorro
node_modules/.bin/babel-node --presets es2015 src/data/AssetsFix.js
# VNX
npm run portfolio
node_modules/.bin/babel-node --presets es2015 src/data/AssetsVNX.js
# VN30
https://bgapidatafeed.vps.com.vn/listvn30
# E1VFVN30
cd broker && node download/E1VFVN30.js && cd ..
```

## Run Filter
```bash
# Terminal output
npm run filter -- --exchange=VNX --method=warren-buffett
# OR output to file
npm run filter -- --exchange=VNX --method=warren-buffett --output=data/filter/warren-buffett.csv
npm run filter -- --exchange=VNX --method=maker --output=data/filter/maker.csv
npm run filter -- --exchange=VNX --method=cashflow --output=data/filter/cashflow.csv
# Save as source
npm run filter -- --exchange=VNX --save=1 --method=warren-buffett
npm run filter -- --exchange=VNX --save=1 --method=canslim
npm run filter -- --exchange=VNX --save=1 --method=lynch
npm run filter -- --exchange=VNX --save=1 --method=graham
npm run filter -- --exchange=VNX --save=1 --method=hi52w
npm run filter -- --exchange=VNX --save=1 --method=liquidity
npm run filter -- --exchange=VNX --save=1 --method=piotroski
```

## Run Model
```bash
python -m model.cli VNX SMB
```

## Developer

### Development Server
```bash
npm run server
```

### Python
```bash
# Install virtualenv
python3 env/virtualenv.pyz env/keras
# Activate
source env/keras/bin/activate
# Freeze
pip freeze > requirements.txt
# Install
pip install -r requirements.txt
# Jupyter
cd notebook
jupyter notebook
screen -m -d python -m notebook --ip 0.0.0.0 --port=8080 --NotebookApp.token=qwertyui --no-browser
```

### Downsize Repo
```bash
git checkout --orphan latest_branch
git add -A
git commit -am "Reinit"
git branch -D master
git branch -m master
git push -f origin master
git gc --aggressive --prune=all
```
