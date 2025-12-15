import { Header } from "@/components/Header";
import { ChatInterface } from "@/components/ChatInterface";
import { Helmet } from "react-helmet";

const Index = () => {
  return (
    <>
      <Helmet>
        <title>TalentScout - AI Hiring Assistant</title>
        <meta 
          name="description" 
          content="TalentScout is an intelligent AI hiring assistant that streamlines candidate screening with personalized technical interviews." 
        />
      </Helmet>
      
      <div className="min-h-screen bg-background flex flex-col relative">
        <Header />
        <ChatInterface />
      </div>
    </>
  );
};

export default Index;
