# **brainpp_yl**: Brain++ API 的简易封装

## ▮ Features
 - [x] split_keys_by_replica: 自动根据是否为 replica 来等比 split keys
    - `keys = __import__('brainpp_yl').split_keys_by_replica(keys)`
 - [x] 可以高效给 PyTorch 的 Dataloader 添加 dpflow
 - [x] brainpp_yl.check_nori: 查看 nori 结构
    - `python -m brainpp_yl.check_nori s3://yl-share/ocrtoc/realsense-v1-1w-blender.nori`
 - [x] nori_pickle_and_put(nori_path, data): 结合 pickle 和 nori
    - 测试用例: `python -c "__import__('brainpp_yl').tools.NoriPickleAndPut.test()"`
 - [x] Cover bpycv result to standard_product_perception nori fromat
    - `bpycv_result_to_spp_nori`

## ▮ Install

```bash
pip install rrun dpflow nori2 redis
git clone git@git-core.megvii-inc.com:yanglei/brainpp_yl.git /tmp/brainpp_yl
pip install /tmp/brainpp_yl

# or: pip install git+ssh://git@git-core.megvii-inc.com:yanglei/brainpp_yl.git
```


## ▮ 注意事项

1. dataloader 的 pin_memory 需要关掉
1. dataloader 的 works 别太大, 最好设置为 0 (太大会在 replica 模式下报错)
1. 在 dpflow_by_dataloader 前, 不要运行任何 `.cuda()` 操作, 所以最好把 dataloader 代码提到 model 前面


## ▮ TODO
 - [ ] 可配置是否允许 IN_RRUN_BRAINPP_YL  内启动 rrun, 或者 IN_RRUN_BRAINPP_YL 作为 deep
 - [ ] 支持 len
 - [ ] 支持自动断掉
 - [ ] duck type dataloader

## Done

