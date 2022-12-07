import React from 'react';
import { Button, Layout } from '@douyinfe/semi-ui';

import ReposGroup from './RepoGroup';
import SideBar from './SideBar';
import TopBar from './TopBar';
import Footer from './Footer';
import SearchBar from './SearchBar';
import Graph from './LineGraph';
import DoubleGraph from './DoublelineGraph'
import RoundGraph from './RoundGraph';
import BarChart from './BarChart'
import { Nav } from '@douyinfe/semi-ui';
import { IconBox, IconUserSetting, IconSimilarity } from '@douyinfe/semi-icons';
import CustomRenderDragDemo from './CustomRenderDragDemo';
import Clouds from './Clouds';
import CompareShowing from './CompareShowing';
import CustomerLogin from './CustomerLogin';
import CardOfName from './CardOfName';
import CustomerPage from './CustomerPage';
import CallLineGraph from './CallLineGraph';
import CallRoundGraph from './CallRoundGraph';
import Allin from './Allin';
import CallBarChart from './CallBarChart';

// npm install react-sortable-hoc -S --legacy-peer-deps

// window.back_url = "http://10.112.35.32:5000"
window.back_url = "http://127.0.0.1:5000"
window.get_commit = "/get_commit/"
window.get_repo = "/get_repo/"
window.get_contributors = "/get_contributors/"
window.get_contributors_all = "/get_contributors/all/"
// window.get_contributors_all = "/contributors/local/"
window.get_user = "/get_user/"
window.get_commit_by_time = "/get_commit_by_time/"
window.get_contributors_core = "/get_contributors/core/"
// window.get_contributors_core = "/contributors/core/"

window.get_cloud = "/cloud/"
window.get_company_commits = "/get_company_commits/"
window.get_update = "/update_repo/"

window.repo_map = 
{
  "https://github.com/pytorch/pytorch" : 0,
  "https://github.com/pytorch/pytorch1" : 1,
  "https://github.com/pytorch/pytorch2" : 2,
  "https://github.com/pytorch/pytorch3" : 3,
  "https://github.com/pytorch/pytorch4" : 4,
  "https://github.com/pytorch/pytorch5" : 5,
  "https://github.com/pytorch/pytorch6" : 6,
  "https://github.com/pytorch/pytorch7" : 7,
  "https://github.com/pytorch/pytorch8" : 8,
  "https://github.com/pytorch/pytorch9" : 9,
  "https://github.com/pytorch/pytorch10" : 10,
  "https://github.com/pytorch/pytorch11" : 11
}

export default function App() {
  const { Sider, Content } = Layout;

  const [repoList, addRepoToList] = React.useState([{
    "id": 1,
    "name": "pytorch",
    "about": "About Tensors and Dynamic neural networks in Python with strong GPU acceleration",
    "link": "https://github.com/pytorch/pytorch"
  }]);

  const [repo_name_list, addRepoNameList] = React.useState
  (
    ["pytorch"]
  )

  const [repo_url_list, addRepoUrlList] = React.useState
  (
    ["https://github.com/pytorch/pytorch"]
  )

  const [lay_out_state, changeLayoutState] = React.useState("Repos");

  function addNewRepo(repo) 
  {
    addRepoToList(repoList.concat(repo))
    addRepoNameList(repo_name_list.concat(repo.name))
    addRepoUrlList(repo_url_list.concat(repo.link))
  }

  function getLayOut()
  {
    if(lay_out_state == "Repos")
    {
      return (
          <Content style={{
            padding: '24px',
            backgroundColor: 'var(--semi-color-bg-0)',
          }}
          >
            <div
              style={{
                borderRadius: '10px',
                border: '1px solid var(--semi-color-border)',
                height: 'auto',
                padding: '32px',
              }}
            >
              <SearchBar onSubmit={addNewRepo} />
              {/* repo数量非常多时，是全部平铺展示而不是在 Content 内部形成下滑条 */}
              <ReposGroup repoList={repoList} />
              {/* <Graph/>
              <DoubleGraph/>
              <RoundGraph/>
              <BarChart/>
  
              <CustomRenderDragDemo />
              <CompareShowing />
              <CustomerLogin />
              <CardOfName></CardOfName> */}
            </div>
          </Content>          
      )
    }
    else if(lay_out_state == "Comparation")
    {
      return (
        <CompareShowing 
          urls = {repo_url_list}
          repo_names = {repo_name_list}
        />
      )
    }
    else if(lay_out_state == "Accounts")
    {
      return (
        <div>
          <CustomerPage></CustomerPage>
        </div>
      )
    }
    else 
    {
      return (
        <div>
          未知状态
        </div>
      )
    }
  }

  const toRepos = () =>
  {
    console.log("repos")
    changeLayoutState("Repos");
  }

  const toComparation = () =>
  {
    changeLayoutState("Comparation");
  }

  const toAccounts = () =>
  {
    changeLayoutState("Accounts");
  }

  function getKey()
  {
    return lay_out_state;
  }


  // // 测试用return
  // return (
  //   // <CallLineGraph repo_name = "hzzz的仓库"></CallLineGraph>
  //   // <div>
  //   //   <CallRoundGraph></CallRoundGraph>
  //   //   <CallRoundGraph is_core = {true}></CallRoundGraph>
  //   // </div>  
  //   <div>
  //     {/* <Allin></Allin> */}
  //     {/* <CompareShowing/> */}
  //     <CallBarChart 
  //       url = "https://github.com/pytorch/pytorch"
  //     ></CallBarChart>
  //   </div>
  // )


  // 真正的return
  return (
    <Layout>

      {/* 这个有点奇怪，分离之后反而显示不对了，你们拿到之后可以先看看怎么修 */}
      {/* <SideBar></SideBar>  */}

      <Sider>
        <Nav
          defaultSelectedKeys={[getKey()]}
          style={{ maxWidth: 200, height: '100%' }}
          items={[
            { itemKey: 'Repos', text: 'Repos', icon: <IconBox size="large" /> , onClick : toRepos},
            { itemKey: 'Comparation', text: 'Comparation', icon: <IconSimilarity size='large' />, onClick : toComparation },
            { itemKey: 'Accounts', text: 'Accounts', icon: <IconUserSetting size="large" /> , onClick : toAccounts },
          ]}
          header={{
            logo: <img alt='logo' src="https://github.githubassets.com/images/modules/logos_page/Octocat.png" />,
            text: 'Github Insight',
          }}
          footer={{
            collapseButton: true,
          }}
        />
      </Sider>

      <Layout>
          <TopBar></TopBar>
          {getLayOut()}
          <Footer></Footer>
      </Layout>
    </Layout>
  );
};
