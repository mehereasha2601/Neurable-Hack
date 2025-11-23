import { useNavigate } from "react-router-dom";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const Index = () => {
  const navigate = useNavigate();

  const ageGroups = [
    {
      id: "child",
      emoji: "👶",
      title: "Child",
      range: "0-10 years",
      description: "Fun stories and calming activities designed for young minds",
      bgColor: "bg-child-bg",
      hoverColor: "hover:bg-child-accent",
    },
    {
      id: "teen",
      emoji: "🧒",
      title: "Teen",
      range: "10-18 years",
      description: "Journaling, art therapy, and mindfulness for adolescents",
      bgColor: "bg-teen-bg",
      hoverColor: "hover:bg-teen-accent",
    },
    {
      id: "adult",
      emoji: "👤",
      title: "Adult",
      range: "18+ years",
      description: "Professional meditation and stress management techniques",
      bgColor: "bg-adult-bg",
      hoverColor: "hover:bg-adult-accent",
    },
  ];

  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-primary via-secondary to-accent flex items-center justify-center p-4">
      <div className="w-full max-w-6xl animate-fade-in">
        <Card className="bg-card/95 backdrop-blur-sm shadow-2xl rounded-3xl p-8 md:p-12">
          {/* Header */}
          <div className="text-center mb-12">
            <div className="text-7xl mb-4 animate-scale-in">🧠</div>
            <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-3">
              Stress Relief Companion
            </h1>
            <p className="text-xl text-muted-foreground">
              Real-time stress monitoring using EEG technology
            </p>
          </div>

          {/* Age Selection Cards */}
          <div className="grid md:grid-cols-3 gap-6 mb-8">
            {ageGroups.map((group) => (
              <Card
                key={group.id}
                className={`${group.bgColor} ${group.hoverColor} border-none cursor-pointer transition-all duration-300 hover:scale-105 hover:shadow-xl p-6 text-center`}
                onClick={() => navigate(`/dashboard/${group.id}`)}
              >
                <div className="text-6xl mb-4">{group.emoji}</div>
                <h3 className="text-2xl font-bold mb-2">{group.title}</h3>
                <p className="text-sm font-semibold mb-3 opacity-70">{group.range}</p>
                <p className="text-sm opacity-80">{group.description}</p>
              </Card>
            ))}
          </div>

          {/* Footer */}
          <div className="text-center text-muted-foreground text-sm space-y-2">
            <p className="flex items-center justify-center gap-3">
              <span>🔒 Your data is secure</span>
              <span className="text-muted">|</span>
              <span>💚 Mental health matters</span>
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default Index;
