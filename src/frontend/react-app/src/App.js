import React from "react";
import { Helmet } from "react-helmet"
import { ToastContainer } from "react-toastify";
import "./App.css";
import NavBar from "./components/NavBar"
import Home from "./pages/Home";
import Repositories from "./pages/Repositories"
import RepoDetail from "./pages/RepoDetail";
import RepoExperimentDetail from "./pages/RepoExperimentDetail";
import { Route } from "wouter";

export default function App() {
    return (
        <div className="App">
            <Helmet>
                <meta charset="utf-8" />
                <title>GTM</title>
                <meta name="description" content="GitHub Text Mining" />
                <meta name="viewport" content="minimum-scale=1, initial-scale=1, width=device-width"/>
            </Helmet>
            <ToastContainer
                limit={1}
                theme="colored"
                position="bottom-right"
                autoClose={2000}
                hideProgressBar={true}
                newestOnTop={true}
                rtl={false}
                pauseOnFocusLoss={false}
                pauseOnHover={false}
            />
            <NavBar />
            <Route component={Home} path="/" />
            <Route component={Repositories} path="/repos" />
            <Route path="/user/:gh_user/repo/:gh_repo">
                {(params) => (
                    <RepoDetail
                        gh_user={params.gh_user}
                        gh_repo={params.gh_repo}
                    />
                )}
            </Route>
            <Route path="/user/:gh_user/repo/:gh_repo/issue/:issue_id/experiment/:task_id">
                {(params) => (
                    <RepoExperimentDetail
                        gh_user={params.gh_user}
                        gh_repo={params.gh_repo}
                        issue_id={params.issue_id}
                        task_id={params.task_id}
                    />
                )}
            </Route>
            <footer className="AppFooter">
                &copy; Created with ♥ by Pablo Fernández
            </footer>
        </div>
    );
}
