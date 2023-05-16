import React from "react";
import Button from "../../components/button/Button";
import "./homepage.css";

const HomePage = () => {
  return (
    <main>
      <div>
        <span>Hey there!</span>
        <h1>This is LinkStack.</h1>
        <p>Too many social links to share? We get it. That's why we created LinkStack. It's your digital business card for all your social media.</p>
        <h3>Ready to declutter your digital life? Sign up and start stacking!</h3>
        <Button theme="main-btn light" text="Get Started" link="/register" />
      </div>
    </main>
  );
};
export default HomePage;
