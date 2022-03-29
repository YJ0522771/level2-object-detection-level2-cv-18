# optimizer
optimizer = dict(
    _delete_=True,
    type='AdamW',
    lr=0.0001,
    betas=(0.9, 0.999),
    weight_decay=0.05,
    paramwise_cfg=dict(
        custom_keys={
            'absolute_pos_embed': dict(decay_mult=0.),
            'relative_position_bias_table': dict(decay_mult=0.),
            'norm': dict(decay_mult=0.)
        }))
# optimizer = dict(type='AdamW', lr=0.0001, momentum=0.9, weight_decay=0.0001)
optimizer_config = dict(grad_clip=None)
# learning policy
# lr_config = dict(
#     policy='step',
#     warmup='linear',
#     warmup_iters=500,
#     warmup_ratio=0.001,
#     step=[16, 22]
# )
lr_config = dict(
    policy='CosineRestart',
    warmup='linear',
    warmup_iters=488,
    warmup_ratio=0.001,
    periods=[1, 12, 24, 36],
    restart_weights=[1,1,0.6,0.3],
    min_lr=0
)
runner = dict(type='EpochBasedRunner', max_epochs=24) # EPOCHS
