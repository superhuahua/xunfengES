import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, hashHistory, IndexRoute } from 'react-router';

import App from './App';

import AssetsTask from './components/AssetsTask';
import VulTask from './components/VulTask';

const routes =
    <Route path={'/'} components={App} >
        <IndexRoute components={AssetsTask}/>
        <Route path={'/vul'} components={VulTask} />
    </Route>;

ReactDOM.render(
    <Router history={hashHistory}>
        {routes}
    </Router>,
    document.getElementById('root')
);