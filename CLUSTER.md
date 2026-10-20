```bash
git clone <url-de-ton-fork> ClassyFridge_Mushroom
cd ClassyFridge_Mushroom
uv venv
uv pip install -r baselines/closed_set/requirements.txt
```

```Shell
mkdir -p data
cd dataset
uv run python download.py --metadata --images --subset "m" --size "300" --save_path "../data"
cd ..
```

```Shell
cd baselines/closed_set
uv run python prepare_metadata.py
```

Doit donner `0/20 images introuvables`

```Shell
uv run python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

Dans `configs/FungiTastic-M-224.yaml` :

* **`epochs`** : entre 30 et 50 (environ 1 minute par epoch sur un bon GPU).
* **`workers`** : le nombre de CPU alloués au job.

```Shell
uv run python train.py \
    --train-path metadata/FungiTastic-Mini-Train.csv \
    --val-path metadata/FungiTastic-Mini-Val.csv \
    --test-path metadata/FungiTastic-Mini-Test.csv \
    --config-path configs/FungiTastic-M-224.yaml \
    --cuda-devices 0
```

Si SLURM:

Mets l’étape 7 dans un fichier `train.sbatch` dans `baselines/closed_set` :

```Shell
#!/bin/bash
#SBATCH --job-name=fungi
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --output=train_%j.log

cd ~/ClassyFridge_Mushroom/baselines/closed_set
uv run python train.py 
    --train-path metadata/FungiTastic-Mini-Train.csv 
    --val-path metadata/FungiTastic-Mini-Val.csv 
    --test-path metadata/FungiTastic-Mini-Test.csv 
    --config-path configs/FungiTastic-M-224.yaml 
    --cuda-devices 0
```

```Shell
sbatch train.sbatch
squeue -u $USER
tail -f train_<jobid>.log
```

À la fin, les checkpoints sont dans baselines/runs/<nom_du_run>/expN/. Pour récupérer best_f1.pth et config.yaml sur ton laptop :

```Shell
scp user@cluster:~/ClassyFridge_Mushroom/baselines/runs/resnet18.a1_in1k-CrossEntropyLoss-vit_heavy/exp1/{best_f1.pth,config.yaml} .
```
