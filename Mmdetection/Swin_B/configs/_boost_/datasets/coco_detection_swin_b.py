dataset_type = 'CocoDataset'

img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)

size_min = 512
size_max = 1024

multi_scale = [(x,x) for x in range(size_min, size_max+1, 32)]

multi_scale_light = [(512,512), (768, 768), (1024, 1024)]

alb_transform = [
    dict(
        type='VerticalFlip',
        p=0.5),
    dict(
        type='HorizontalFlip',
        p=0.5),
    dict(
        type='OneOf',
        transforms=[
            dict(
                type='GaussNoise',
                p=1.0),
            dict(
                type='GaussianBlur',
                p=1.0),
            dict(
                type='Blur',
                p=1.0)
        ],
        p=0.1),
    dict(
        type='OneOf',
        transforms=[
            dict(
                type='RandomGamma',
                p=1.0),
            dict(
                type='HueSaturationValue',
                p=1.0),
            dict(
                type='ChannelDropout',
                p=1.0),
            dict(
                type='ChannelShuffle',
                p=1.0),
            dict(
                type='RGBShift',
                p=1.0)
        ],
        p=0.1),
    dict(
        type='OneOf',
        transforms=[
            dict(
                type='ShiftScaleRotate',
                p=1.0),
            dict(
                type='RandomRotate90',
                p=1.0),
        ],
        p=0.1)
]

train_pipeline = [
    # dict(type='LoadImageFromFile'),
    # dict(type='LoadAnnotations', with_bbox=True),
    # dict(type='MixUp',
    #     img_scale = (1024,1024),
    #     # ratio_range = (0.8),(1.6),
    #     pad_val=114),
    # dict(
    #     type='Mosaic',
    #     img_scale = (1024,1024),
    #     pad_val=114),

    dict(type='Resize', img_scale=multi_scale, multiscale_mode='value', keep_ratio=True),
    dict(
    type='Albu',
    transforms=alb_transform,
    bbox_params=dict(
        type='BboxParams',
        format='pascal_voc',
        label_fields=['gt_labels'],
        min_visibility=0.0,
        filter_lost_elements=True),
    keymap={
            'img': 'image',
            'gt_bboxes': 'bboxes'
    },
    update_pad_shape=False,
    skip_img_without_anno=True),
    dict(type='RandomFlip', flip_ratio=0.5),
    dict(type='Normalize', **img_norm_cfg),
    # mosaic?
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels']),
]

test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=multi_scale_light,
        flip=True,
        transforms=[
            dict(type='Resize', img_scale=multi_scale_light, multiscale_mode='value', keep_ratio=True),
            dict(type='RandomFlip'),
            dict(type='Normalize', **img_norm_cfg),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img']),
        ])
]

classes = ('General trash', 'Paper', 'Paper pack', 'Metal', 'Glass', 'Plastic', 'Styrofoam', 'Plastic bag', 'Battery', 'Clothing')

data = dict(
    samples_per_gpu=4,
    workers_per_gpu=2,
    train=dict(
        # type=dataset_type,
        type = 'MultiImageMixDataset',
        dataset = dict(
            type=dataset_type,
            classes=classes,
            # ann_file=kfold_root + f'cv_train_{fold_num}.json',
            ann_file=data_root + 'train_new.json',
            img_prefix=data_root,
            pipeline=[dict(type='LoadImageFromFile'),
                      dict(type='LoadAnnotations', with_bbox=True)
            ],
            filter_empty_gt=False
        ),
        pipeline=train_pipeline),

    
    val=dict(
        type=dataset_type,
        classes=classes,
        ann_file=kfold_root + f'cv_val_{fold_num}.json',
        img_prefix=data_root,
        pipeline=test_pipeline),
    
    test=dict(
        type=dataset_type,
        classes=classes,
        ann_file=kfold_root + f'cv_val_{fold_num}.json',
        img_prefix=data_root,
        pipeline=test_pipeline))