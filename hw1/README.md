# dl_frameworks_dp

Домашнее задание 1.

Project Organization
------------

    ├── .dvc                               <- dvc folder
    │
    ├── data                               <- directory for data
    │   ├── data_prep.ipynb                <- notebook for data preparation
    │   └── Ethos_Dataset_Binary.csv.dvc   <- dvc file for data
    │
    ├── model_params                       <- directory for parametrs of models
    │   ├── baseline_model_params.json.dvc <- dvc file for parametrs of base model
    │   └── tuned_model_params.json.dvc    <- dvc file for parametrs of tuned model
    │
    ├── models                             <- directory for models
    │   ├── LGBMC_baseline_model.pkl.dvc   <- dvc file of base model
    │   └── LGBMC_tuned_model.pkl.dvc      <- dvc file of tuned model
    │
    ├── hw1.ipynb                          <- notebook with model optimization process
    │
    ├── README.md                          <- The README - report
    │
    ├── summary_report.txt                 <- report on models
    │
    └── requirements.txt                   <- The requirements file for reproducing the analysis environment

--------

# Что сделано
Код реализован на **pandas**.
[Датасет](https://github.com/intelligence-csd-auth-gr/Ethos-Hate-Speech-Dataset/blob/master/ethos/ethos_data/Ethos_Dataset_Binary.csv)
разделен на train/test в соотношении 70/30.

Для обучения регрессора были использованы признаки, полученные из TfidfVectorizer.

Модель для обучения - LGBMClassifier.
Бэйзлайн с параметрами по умолчанию и learning_rate=0.5.
Подбор гиперпараметровя с помощью библиотеки **Optuna**, метрика, по которой проводилась оптимизация - accuracy, 
также измерялись f1-score и roc-auc score. Результаты представлены ниже.

| Метрика  | Train_baseline | Test_baseline | Train_runed |  Test_tuned   |
|:--------:|:--------------:|:-------------:|:-----------:|:-------------:|
| accuracy |    0.921203    |      0.8      |  0.918338   | **0.803333**  | 
| f1-score |    0.910336    |   0.779239    |  0.906863   | **0.781414**  | 
| roc-auc  |    0.972565    |   0.819483    |  0.965560   | **0.842506**  | 

При этом оптимизировались следующие гиперпараметры:
- "objective"
- "boosting_type"
- "n_estimators"
- "learning_rate"
- "num_leaves"
- "max_depth"

Настроен DVC-репозиторий в google drive, загружены все артефакты.

Подготовлен summary report.