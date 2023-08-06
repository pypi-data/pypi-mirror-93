<h1 align="center">
  <a href="https://pypi.org/project/pycomp/#description"><img src="https://i.imgur.com/WcAaq1P.png" alt="pycomp Logo"></a>
</h1>

<div align="center">
  <strong>Fábrica de componentes Python</strong>
</div>
<br/>

<div align="center">
  
![Release](https://img.shields.io/badge/release-ok-brightgreen)
[![PyPI](https://img.shields.io/pypi/v/pycomp?color=blueviolet)](https://pypi.org/project/pycomp/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pycomp?color=9cf)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pycomp?color=green)
![PyPI - Status](https://img.shields.io/pypi/status/pycomp)

</div>
<br/>

Literalmente, uma fábrica de componentes em Python criada para auxiliar implementações, automações e até treinamento de modelos de Machine Learning! O objetivo desse pacote é propor uma forma mais fácil de se trabalhar com Python a partir do fornecimento de componentes prontos (funções e classes) para uma série de atividades rotineiras e exploratórias.

## Features

- :file_folder: __fs__: módulo responsável por auxiliar o manuseio de arquivos em sistemas operacionais. Em seu conteúdo, é possível encontrar funções úteis para a cópia de arquivos de um diretório origem para um diretório destino, além de funções utilizadas para a validação de presença e atualização de arquivos, entre outras.

- :pencil: __log__: módulo com o objetivo de facilitar a geração, configuração e o armazenamento de logs de execução dos demais módulos do pacote.
  
- :robot: __ml__: provavelmente o mais completo do pacote, o módulo ml (machine learning) contém componentes apropriados para a construção e aplicação de pipelines de pré-processamento de dados, além de blocos de código responsáveis por automatizar o treinamento e avaliação de modelos de aprendizado de máquina. 
  
- :bar_chart: __viz__: módulo responsável por propor componentes prontos para geração e customização de gráficos utilizando as bibliotecas matplotlib e seaborn. As funções contidas neste módulo trazem códigos consolidados para geração de insights em bases de dados a partir de análises gráficas personalizadas. 

A fábrica está a todo vapor! Com mais de 2 mil linhas de código, sua capacidade de produção e seu leque de fornecimento pode ser resumido em:

| Tópico                     | Módulo                   | Funções           | Classes         | Componentes Totais  |Linhas de Código |
| -------------------------- | :---------------:        | :---------------: | :-------------: | :-----------------: | :-------------: |
| File System                | `pycomp.fs.arquivos`     |         4         |        0        |        4            |      ~300       |
| Logs                       | `pycomp.log.log_config`  |         1         |        0        |        1            |       ~70       |
| Machine Learning           | `pycomp.ml.transformers` |         0         |        9        |        9            |      ~400       |
|                            | `pycomp.ml.trainer`      |        25         |        1        |       26            |     ~1500       |
| Viz                        | `pycomp.viz.formatador`  |         2         |        1        |        3            |      ~100       |
|                            | `pycomp.viz.insights`    |         5         |        0        |        5            |      ~700       |


## Instalação

A última versão do pacote `pycomp` encontra-se publicada no repositório [PyPI](https://pypi.org/project/pycomp/). 

> **Nota**: Como boa prática, recomenda-se a criação de um ambiente virual env Python para alocar as bibliotecas do projeto a ser desenvolvido. Caso não tenha um virtual env criado, o bloco de código abaixo pode ser utilizado para a criação de ambiente virtual em um diretório específico: 
```bash
# Criando diretório para o virtual env
$ mkdir ~/<nome diretorio> # ou qualquer outro caminho
$ cd ~/<nome diretorio>

# Criando ambiente virtual
$ python3 -m venv <nome venv>
```

Utilizando uma ferramenta de desenvolvimento (IDE ou a própria linha de comando), ative o ambiente virtual de trabalho:
```bash
$ source ~/<nome diretorio>/<nome venv>/bin/activate
```

Após a ativação, é possível instalar o pacote `pycomp` via pip:
```bash
# Atualizando pip e instalando pycomp
$ pip install pycomp --upgrade
```

> **Nota**: o pacote `pycomp` é construído como uma ferramenta de top level em cima de outros pacotes conhecidos em Python, como sklearn, pandas e numpy. Ao instalar o `pycomp`, as dependências especificadas também serão instaladas automaticamente em seu ambiente virtual de trabalho.

Resumo do output esperado no cmd após a instalação do pacote::
```
Collecting pycomp
[...]
Installing collected packages: numpy, pytz, six, python-dateutil, pandas, joblib, scipy, threadpoolctl, scikit-learn, tqdm, slicer, llvmlite, numba, shap, pyparsing, cycler, certifi, kiwisolver, pillow, matplotlib, seaborn, pycomp
  Running setup.py install for numba ... done
  Running setup.py install for shap ... done
Successfully installed certifi-2020.11.8 cycler-0.10.0 joblib-0.17.0 kiwisolver-1.3.1 llvmlite-0.34.0 matplotlib-3.3.2 numba-0.51.2 numpy-1.19.3 pandas-1.1.3 pillow-8.0.1 pycomp-0.0.15 pyparsing-2.4.7 python-dateutil-2.8.1 pytz-2020.4 scikit-learn-0.23.2 scipy-1.5.4 seaborn-0.11.0 shap-0.37.0 six-1.15.0 slicer-0.0.3 threadpoolctl-2.1.0 tqdm-4.51.0
```

## Utilização
Para demonstrar uma poderosa aplicação do pacote `pycomp`, será exemplificado abaixo um trecho de código que, em poucas linhas, é responsável por:
  - Consolidar um Pipeline completo de DataPrep utilizando classes _transformadoras_ já preparadas
  - Treinar e avaliar diferentes modelos de classificação (_LogisticRegression, DecisionTreeClassifier_ e _RandomForestClassifier_)
  - Utilização de _RandomizedSearchCV_ para buscar os melhores hyperparâmetros para cada modelo
  - Registrar os resultados obtidos (dados e gráficos) em um diretório de output
  - Retornar um modelo específico para passos futuros
  
Como insumo, será utilizado o dataset [Titanic](https://www.kaggle.com/c/titanic) obtido a partir da união dos arquivos `train.csv` e `test.csv`, gerando assim o input `titanic.csv` contido no script.

```python
# Importando bibliotecas
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from warnings import filterwarnings
filterwarnings('ignore')

from pycomp.ml.transformers import FormataColunas, FiltraColunas, DefineTarget, EliminaDuplicatas, PreencheDadosNulos, SplitDados
from pycomp.ml.trainer import ClassificadorBinario

# Lendo base de dados (titanic data - train + test)
df = pd.read_csv('titanic.csv')
cols_filter = ['survived', 'pclass', 'age', 'sibsp', 'fare']

# Pipeline da primeira camada
first_layer_pipe = Pipeline([
    ('formatter', FormataColunas()),
    ('selector', FiltraColunas(features=cols_filter)),
    ('target_generator', DefineTarget(target_col='survived', pos_class=1.0)),
    ('dup_dropper', EliminaDuplicatas()),
    ('na_filler', PreencheDadosNulos(value_fill=0)),
    ('splitter', SplitDados(target='target'))
])

# Executando pipeline
X_train, X_test, y_train, y_test = first_layer_pipe.fit_transform(df)
features = list(X_train.columns)

# Preparando classificadores
tree_clf = DecisionTreeClassifier()
log_reg = LogisticRegression()
forest_clf = RandomForestClassifier()

# Logistic Regression hyperparameters
logreg_param_grid = {
    'C': np.linspace(0.1, 10, 20),
    'penalty': ['l1', 'l2'],
    'class_weight': ['balanced', None],
    'random_state': [42],
    'solver': ['liblinear']
}

# Decision Trees hyperparameters
tree_param_grid = {
    'criterion': ['entropy', 'gini'],
    'max_depth': [3, 5, 10, 20],
    'max_features': np.arange(1, X_train.shape[1]),
    'class_weight': ['balanced', None],
    'random_state': [42]
}

# Random Forest hyperparameters
forest_param_grid = {
    'bootstrap': [True, False],
    'max_depth': [3, 5, 10, 20, 50],
    'n_estimators': [50, 100, 200, 500],
    'random_state': [42],
    'max_features': ['auto', 'sqrt'],
    'class_weight': ['balanced', None]
}

# Configurando classificadores
set_classifiers = {
    'LogisticRegression': {
        'model': log_reg,
        'params': logreg_param_grid
    },
    'DecisionTree': {
        'model': tree_clf,
        'params': tree_param_grid
    },
    'RandomForest': {
        'model': forest_clf,
        'params': forest_param_grid
    }
}

# Definindo variáveis de execução
OUTPUT_PATH = 'output/'

# Inicializando objeto
trainer = ClassificadorBinario()

# Fluxo de treino
trainer.training_flow(set_classifiers, X_train, y_train, X_test, y_test, features, output_path=OUTPUT_PATH, random_search=True)

# Análise gŕafica
trainer.visual_analysis(features=features, model_shap='DecisionTree', output_path=OUTPUT_PATH)

# Retornando informações relevantes de um modelo específico
model = trainer._get_estimator(model_name='RandomForest')
metrics = trainer._get_metrics(model_name='RandomForest')
model_info = trainer._get_model_info(model_name='RandomForest')
classifiers_info = trainer._get_classifiers_info()
```

Ao utilizar as ferramentas disponibilizadas no módulo `ml` do pacote `pycomp`, o usuário consegue facilmente construir e executar um Pipeline de preparação de dados enxuto e otimizado a partir das classes pré definidas no módulo `transformers`. Em complemento a essa feature, o módulo `trainer` traz consigo a classe `ClassificadorBinario` com o objetivo de facilitar o treinamento e avaliação de classificadores binários. O usuário final necessita apenas fornecer uma base de dados como input, os _estimators_ (modelos a serem treinados) e seus respectivos hyperparâmetros de busca a serem utilizados no processo. 

### Outputs
Ao realizar a importação do pacote `pycomp` no script, um objeto logger da biblioteca `logging` é instanciado automaticamente, gerando assim um arquivo `exec_log/execution_log.log` no mesmo diretório de execução do script com os detalhes de cada passo dado nas funções e métodos aplicados. A cada execução do exemplo acima, espera-se que as seguintes mensagens sejam registradas no arquivo de log apresentadas no cmd:

```
DEBUG;2020-11-15 09:25:05;trainer.py;trainer;224;Treinando modelo LogisticRegression
DEBUG;2020-11-15 09:25:05;trainer.py;trainer;236;Aplicando RandomizedSearchCV
[Parallel(n_jobs=-1)]: Using backend LokyBackend with 4 concurrent workers.
[Parallel(n_jobs=-1)]: Done  50 out of  50 | elapsed:    1.2s finished
DEBUG;2020-11-15 09:25:06;trainer.py;trainer;248;Salvando arquivo pkl do modelo LogisticRegression treinado
DEBUG;2020-11-15 09:25:06;trainer.py;trainer;132;Salvando modelo pkl no diretório especificado
DEBUG;2020-11-15 09:25:06;trainer.py;trainer;224;Treinando modelo DecisionTree
DEBUG;2020-11-15 09:25:06;trainer.py;trainer;236;Aplicando RandomizedSearchCV
[Parallel(n_jobs=-1)]: Using backend LokyBackend with 4 concurrent workers.
[Parallel(n_jobs=-1)]: Done  50 out of  50 | elapsed:    0.2s finished
DEBUG;2020-11-15 09:25:06;trainer.py;trainer;248;Salvando arquivo pkl do modelo DecisionTree treinado
DEBUG;2020-11-15 09:25:06;trainer.py;trainer;132;Salvando modelo pkl no diretório especificado
DEBUG;2020-11-15 09:25:06;trainer.py;trainer;224;Treinando modelo RandomForest
[...]
DEBUG;2020-11-15 09:26:36;trainer.py;trainer;1145;Plotando curvas de aprendizado de treino e validação para o modelo RandomForest
DEBUG;2020-11-15 09:26:36;trainer.py;trainer;172;Salvando imagem no diretório especificado
INFO;2020-11-15 09:26:37;trainer.py;trainer;176;Imagem salva com sucesso em output/imgs/learning_curve.png
DEBUG;2020-11-15 09:26:37;trainer.py;trainer;1187;Explicando o modelo DecisionTree através da análise shap
DEBUG;2020-11-15 09:26:37;trainer.py;trainer;1195;Retornando parâmetros da classe para o modelo DecisionTree
DEBUG;2020-11-15 09:26:37;trainer.py;trainer;1205;Criando explainer e gerando valores shap para o modelo DecisionTree
DEBUG;2020-11-15 09:26:38;trainer.py;trainer;1218;Plotando análise shap para o modelo DecisionTree
DEBUG;2020-11-15 09:26:38;trainer.py;trainer;172;Salvando imagem no diretório especificado
INFO;2020-11-15 09:26:38;trainer.py;trainer;176;Imagem salva com sucesso em output/imgs/shap_analysis_DecisionTree.png
DEBUG;2020-11-15 09:26:38;trainer.py;trainer;1305;Retornando estimator do modelo RandomForest já treinado
DEBUG;2020-11-15 09:26:38;trainer.py;trainer;1326;Retornando as métricas dos modelos treinados
DEBUG;2020-11-15 09:26:38;trainer.py;trainer;1366;Retornando informações registradas do modelo RandomForest
```

Ao definir um diretório de saída, as execuções dos métodos `training_flow()` e `visual_analysis()` da classe `ClassificadorBinario` irão gerar arquivos úteis para uma definitiva avaliação do melhor classificador para a respectiva tarefa. No código utilizado como exemplo, a variável `OUTPUT_PATH` recebe a string `'output/'` e, por consequência, gera os seguintes arquivos ao final da execução:

```bash
$ tree output/
output/
├── imgs
│   ├── confusion_matrix.png
│   ├── feature_importance.png
│   ├── learning_curve.png
│   ├── metrics_comparison.png
│   ├── roc_curve.png
│   ├── score_bins_percent.png
│   ├── score_bins.png
│   ├── score_distribution.png
│   └── shap_analysis_DecisionTree.png
├── metrics
│   ├── metrics.csv
│   └── top_features.csv
└── models
    ├── decisiontree.pkl
    ├── logisticregression.pkl
    └── randomforest.pkl
```

## Próximos Passos
- [x] Consolidar função `visual_analysis()` para gerar todas as análises acima (`trainer.py`)
- [x] Consturção de funções para análise categórica em processo de EDA (`insights.py`)
- [x] Criação de guideline para utilização do módulo `transformers.py`
- [x] Criação de guideline para utilização do módulo `trainer.py`
- [x] Criação de guideline para utilização do módulo `insights.py`
- [ ] Brainstorming para pipelines automáticos de prep + treino (`transformers.py + trainer.py`)
- [ ] Inserir GIF de demonstração do projeto
- [ ] Finalização do módulo insights para plotagens gráficas e aplicação de EDA em bases de dados (`insights.py`)


## Guidelines
De modo a propor uma maior democratização do pacote `pycomp`, foram construídos alguns "notebooks-guidelines" em espécies de demonstração das principais aplicações dos módulos `pycomp` em situações prática de uso. Assim, na pastas `guidelines/` do projeto no Github, é possível encontrar diferentes arquivos `.ipynb` contendo:

- `insights_guideline.ipynb`: aplicação do módulo _insights.py_ para a construção de plotagens gráficos dentro de um processo de exploração de uma base de dados em caráter investigativo, analisando os dados e propondo insights para possíveis problemas de negócio.
- `transformers_guideline.ipynb`: em complemento ao módulo _insights.py_, o módulo _transformers.py_ atua na continuação na cadeia de desenvolvimento de uma solução completa em ciência de dados. Neste notebook explicativo, o objetivo é construir um pipeline completo de transformação de uma base de dados lida.
- `trainer_guideline.ipynb`: por fim, finalizando o desenvolvimento da solução, o notebook explicativo para o módulo _trainer.py_ atua de modo a evidenciar um exemplo prático de treinamento e avaliação de um modelo preditivo em uma base já preparada a partir de um pipeline construído previamente com as ferramentas do módulo _transformers.py_


## Referências

Géron A., ed. (2017) Hands-On Machine Learning with Scikit-Learn & TensorFlow. 1st ed. California: O'Reilly

Géron A., handson-ml, (2020), GitHub repository, https://github.com/ageron/handson-ml  	

Stanford University (Producer). (2019). Machine Learning. Retrieved from https://www.coursera.org/learn/machine-learning/home/welcome
