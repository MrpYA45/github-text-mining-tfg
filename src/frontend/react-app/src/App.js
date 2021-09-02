import React from "react";
import { Helmet } from "react-helmet"
import { ToastContainer } from "react-toastify";
import "./App.css";
import Home from "./pages/Home";
import RepoDetail from "./pages/RepoDetail";
import { Route } from "wouter";

export default function App() {
    return (
        <div className="App">
            <Helmet>
                <title>GTM</title>
                <meta name="description" content="GitHub Text Mining" />
                <meta name="viewport" content="minimum-scale=1, initial-scale=1, width=device-width"/>
            </Helmet>
            <ToastContainer
                limit={1}
                theme="colored"
                position="bottom-right"
                autoClose={4000}
                hideProgressBar={true}
                newestOnTop={true}
                rtl={false}
                pauseOnFocusLoss={false}
                pauseOnHover={false}
            />
            <Route component={Home} path="/" />
            <Route path="/user/:gh_user/repo/:gh_repo">
                {(params) => (
                    <RepoDetail
                        gh_user={params.gh_user}
                        gh_repo={params.gh_repo}
                    />
                )}
            </Route>
            <Route component={Home} path="/test" />
            <footer className="App-footer">
                &copy; Created with ♥ by Pablo Fernández
            </footer>
        </div>
    );
}
