import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Settings, ArrowLeft } from "lucide-react";
import ChildIntervention from "@/components/interventions/ChildIntervention";
import TeenIntervention from "@/components/interventions/TeenIntervention";
import AdultIntervention from "@/components/interventions/AdultIntervention";
import CrisisModal from "@/components/CrisisModal";

type AgeGroup = "child" | "teen" | "adult";
type StressLevel = "calm" | "stressed" | "extreme";

const Dashboard = () => {
  const { ageGroup } = useParams<{ ageGroup: AgeGroup }>();
  const navigate = useNavigate();
  
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [stressLevel, setStressLevel] = useState<StressLevel>("calm");
  const [stressValue, setStressValue] = useState(0.2);
  const [showIntervention, setShowIntervention] = useState(false);
  const [showCrisis, setShowCrisis] = useState(false);
  const [readingsCount, setReadingsCount] = useState(0);
  const [sessionDuration, setSessionDuration] = useState(0);

  // Simulate stress monitoring
  useEffect(() => {
    if (!isMonitoring) return;

    const interval = setInterval(() => {
      // Simulate random stress values
      const newValue = Math.random();
      setStressValue(newValue);
      setReadingsCount(prev => prev + 1);
      
      if (newValue < 0.4) {
        setStressLevel("calm");
        setShowIntervention(false);
      } else if (newValue < 0.7) {
        setStressLevel("stressed");
        setShowIntervention(true);
      } else {
        setStressLevel("extreme");
        setShowIntervention(true);
        
        // Show crisis modal if extreme for too long
        setTimeout(() => {
          if (stressLevel === "extreme") {
            setShowCrisis(true);
          }
        }, 3000);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [isMonitoring, stressLevel]);

  // Track session duration
  useEffect(() => {
    if (!isMonitoring) return;
    const timer = setInterval(() => {
      setSessionDuration(prev => prev + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, [isMonitoring]);

  const getStatusEmoji = () => {
    switch (stressLevel) {
      case "calm": return "😊";
      case "stressed": return "😰";
      case "extreme": return "🚨";
    }
  };

  const getStatusText = () => {
    switch (stressLevel) {
      case "calm": return "CALM";
      case "stressed": return "STRESSED";
      case "extreme": return "EXTREME";
    }
  };

  const getStatusColor = () => {
    switch (stressLevel) {
      case "calm": return "bg-calm";
      case "stressed": return "bg-stressed";
      case "extreme": return "bg-extreme";
    }
  };

  const ageGroupInfo = {
    child: { label: "Child (0-10)", color: "bg-child-accent" },
    teen: { label: "Teen (10-18)", color: "bg-teen-accent" },
    adult: { label: "Adult (18+)", color: "bg-adult-accent" },
  };

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (!ageGroup || !["child", "teen", "adult"].includes(ageGroup)) {
    return <div>Invalid age group</div>;
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Top Bar */}
      <header className="bg-card border-b border-border px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => navigate("/")}
          >
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <h1 className="text-2xl font-bold">Stress Relief Companion</h1>
        </div>
        <div className="flex items-center gap-4">
          <Badge className={`${ageGroupInfo[ageGroup].color} text-foreground`}>
            {ageGroupInfo[ageGroup].label}
          </Badge>
          <Button variant="ghost" size="icon">
            <Settings className="h-5 w-5" />
          </Button>
        </div>
      </header>

      {/* Main Layout */}
      <div className="p-6">
        <div className="grid lg:grid-cols-3 gap-6 mb-6">
          {/* Status Card */}
          <Card className={`p-6 ${stressLevel === "extreme" ? "animate-pulse-soft" : ""}`}>
            <div className="text-center space-y-4">
              <div className="text-8xl mb-4">{getStatusEmoji()}</div>
              <h2 className="text-3xl font-bold">{getStatusText()}</h2>
              
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Stress Level</span>
                  <span className="font-semibold">{(stressValue * 100).toFixed(0)}%</span>
                </div>
                <Progress 
                  value={stressValue * 100} 
                  className={`h-3 ${getStatusColor()}`}
                />
              </div>

              <div className="pt-4 space-y-2 text-sm text-muted-foreground">
                <div className="flex justify-between">
                  <span>Signal Quality</span>
                  <span className="text-foreground font-medium">Good</span>
                </div>
                <div className="flex justify-between">
                  <span>Baseline</span>
                  <span className="text-foreground font-medium">0.25</span>
                </div>
              </div>
            </div>
          </Card>

          {/* Graph Area */}
          <Card className="p-6">
            <h3 className="text-xl font-semibold mb-4">Stress Level Over Time</h3>
            <div className="h-64 bg-gradient-to-br from-primary/10 to-secondary/10 rounded-lg flex items-center justify-center text-muted-foreground">
              Real-time graph will appear here
            </div>
          </Card>

          {/* Controls */}
          <Card className="p-6 space-y-4">
            <Button
              className={`w-full h-16 text-lg font-semibold ${
                isMonitoring 
                  ? "bg-destructive hover:bg-destructive/90" 
                  : "bg-calm hover:bg-calm/90"
              }`}
              onClick={() => {
                setIsMonitoring(!isMonitoring);
                if (!isMonitoring) {
                  setReadingsCount(0);
                  setSessionDuration(0);
                }
              }}
            >
              {isMonitoring ? "⏹️ Stop Monitoring" : "▶️ Start Monitoring"}
            </Button>

            <Button variant="outline" className="w-full">
              🔄 New Session
            </Button>

            <Button variant="outline" className="w-full">
              📖 View Journal History
            </Button>

            {isMonitoring && (
              <Card className="p-4 bg-muted">
                <h4 className="font-semibold mb-3">Session Stats</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span>Readings</span>
                    <span className="font-medium">{readingsCount}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Duration</span>
                    <span className="font-medium">{formatDuration(sessionDuration)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Avg Stress</span>
                    <span className="font-medium">{(stressValue * 100).toFixed(0)}%</span>
                  </div>
                </div>
              </Card>
            )}
          </Card>
        </div>

        {/* Intervention Panel */}
        {showIntervention && (
          <div className="animate-scale-in">
            {ageGroup === "child" && <ChildIntervention onClose={() => setShowIntervention(false)} />}
            {ageGroup === "teen" && <TeenIntervention onClose={() => setShowIntervention(false)} />}
            {ageGroup === "adult" && <AdultIntervention onClose={() => setShowIntervention(false)} />}
          </div>
        )}
      </div>

      {/* Crisis Modal */}
      <CrisisModal 
        open={showCrisis} 
        onOpenChange={setShowCrisis}
        onContinue={() => setShowCrisis(false)}
        onStop={() => {
          setShowCrisis(false);
          setIsMonitoring(false);
        }}
      />
    </div>
  );
};

export default Dashboard;
