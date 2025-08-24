import React from 'react';

const ErrorMessage = ({ message }) => (
  <div className="bg-red-500/20 border border-red-500/30 text-red-100 p-4 rounded-lg my-4 backdrop-blur-sm" role="alert">
    <p className="font-bold">An Error Occurred</p>
    <p>{message}</p>
  </div>
);

export default ErrorMessage;
