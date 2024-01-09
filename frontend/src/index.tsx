import React from 'react';
import ReactDOM from 'react-dom/client';
import CreateLogin from './routes/CreateLogin'
import ConnectLogin from './routes/ConnectLogin'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import ErrorPage from "./error-page";
import Chat from "./routes/Chat"

const router = createBrowserRouter([
  {
    path: "/create_chat",
    element: <CreateLogin />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/connect_chat",
    element: <ConnectLogin />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/chat/:chatName",
    element: <Chat />,
  },
]);

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
    <RouterProvider router={router} />
);
