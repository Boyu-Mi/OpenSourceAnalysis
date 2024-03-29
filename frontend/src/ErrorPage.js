import React from 'react';
import { Empty, Button } from '@douyinfe/semi-ui';
import { IllustrationNoResult } from '@douyinfe/semi-illustrations';

export default function ErrorPage() {
    return (
        <div style={{display: 'flex', flexWrap: 'wrap'}}>
            <Empty
                title={'仓库链接有误'}
                image={<IllustrationNoResult style={{width: 200, height: 200}}/>}
                layout="horizontal"
                description="你在知识的荒原中迷失了方向……"
                style={{width: 500, margin: 'auto', padding: 100,}}
            >
            </Empty>
        </div>
    );
}