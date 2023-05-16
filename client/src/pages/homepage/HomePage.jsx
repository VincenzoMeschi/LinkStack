import React from "react";
import Button from "../../components/button/Button";
import HeroImg from "../../images/LinkStack-isometric.png";
import "./homepage.css";

const HomePage = () => {
  return (
    <main>
      <div className="hero-img">
        <img src={HeroImg} alt="Link Stack hero section isometric image" />
      </div>
      <div className="hero-text">
        <span>Hey there!</span>
        <h1>
          This is <span>LinkStack.</span>
        </h1>
        <p>Too many social links to share? We get it. That's why we created LinkStack. It's your digital business card for all your social media.</p>
        <h3>Ready to declutter your digital life? Sign up and start stacking!</h3>
        <Button theme="main-btn light" text="Get Started" link="/register" />
      </div>
    </main>
  );
};
export default HomePage;
