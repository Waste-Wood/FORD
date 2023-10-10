 torchrun --nproc_per_node=4 few_shot_vicuna.py --task socialiqa
 torchrun --nproc_per_node=4 few_shot_vicuna.py --task piqa
 torchrun --nproc_per_node=4 few_shot_vicuna.py --task strategyqa

 torchrun --nproc_per_node=4 llama_official.py --task anli
 torchrun --nproc_per_node=4 llama_official.py --task csqa
 torchrun --nproc_per_node=4 llama_official.py --task copa
 torchrun --nproc_per_node=4 llama_official.py --task ecare
 torchrun --nproc_per_node=4 llama_official.py --task socialiqa
 torchrun --nproc_per_node=4 llama_official.py --task piqa
 torchrun --nproc_per_node=4 llama_official.py --task strategyqa
