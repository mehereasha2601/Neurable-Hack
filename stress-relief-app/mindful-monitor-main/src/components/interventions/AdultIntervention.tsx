import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { CheckCircle2, Play, Pause } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface AdultInterventionProps {
  onClose: () => void;
}

const bodyParts = [
  "feet", "calves", "thighs", "hips", "abdomen", "chest", 
  "shoulders", "arms", "hands", "neck", "face", "head"
];

const AdultIntervention = ({ onClose }: AdultInterventionProps) => {
  const { toast } = useToast();
  const [isScanning, setIsScanning] = useState(false);
  const [currentPart, setCurrentPart] = useState(0);
  const [scanProgress, setScanProgress] = useState(0);

  const startBodyScan = () => {
    setIsScanning(true);
    setCurrentPart(0);
    setScanProgress(0);

    const interval = setInterval(() => {
      setScanProgress((prev) => {
        const newProgress = prev + (100 / bodyParts.length);
        if (newProgress >= 100) {
          clearInterval(interval);
          setIsScanning(false);
          toast({
            title: "Body scan complete",
            description: "How do you feel?",
          });
          return 100;
        }
        return newProgress;
      });

      setCurrentPart((prev) => {
        const next = prev + 1;
        return next >= bodyParts.length ? prev : next;
      });
    }, 3000);
  };

  const pauseScan = () => {
    setIsScanning(false);
  };

  return (
    <Card className="border-l-4 border-l-adult-accent bg-card shadow-lg">
      <div className="p-6">
        {/* Header */}
        <div className="mb-6">
          <h2 className="text-2xl font-semibold text-foreground mb-2">
            Take a moment for yourself
          </h2>
          <p className="text-muted-foreground">
            Professional stress relief techniques
          </p>
        </div>

        {/* Tabs */}
        <Tabs defaultValue="body-scan" className="w-full">
          <TabsList className="grid w-full grid-cols-4 mb-6">
            <TabsTrigger value="reading">📖 Reading</TabsTrigger>
            <TabsTrigger value="meditation">🧘 Meditation</TabsTrigger>
            <TabsTrigger value="body-scan">🫁 Body Scan</TabsTrigger>
            <TabsTrigger value="journal">📝 Journal</TabsTrigger>
          </TabsList>

          <TabsContent value="reading" className="space-y-4">
            <Card className="p-6 bg-muted">
              <div className="prose prose-lg max-w-none">
                <p className="text-lg leading-relaxed">
                  Mindfulness content: When stress rises, remember that you have the power to pause. 
                  Take three deep breaths. Notice the sensation of air entering and leaving your body. 
                  This moment is yours.
                </p>
              </div>
            </Card>
          </TabsContent>

          <TabsContent value="meditation" className="space-y-4">
            <Card className="p-6 bg-muted text-center">
              <div className="text-5xl mb-4">🧘</div>
              <h3 className="text-xl font-semibold mb-2">5-7 Minute Guided Meditation</h3>
              <p className="text-muted-foreground mb-4">
                Find a comfortable position and focus on your breath
              </p>
              <Button className="w-full h-12">▶️ Start Meditation</Button>
            </Card>
          </TabsContent>

          <TabsContent value="body-scan" className="space-y-6">
            <Card className="p-6 bg-gradient-to-br from-adult-bg to-background">
              <h3 className="text-xl font-semibold mb-2">15-Minute Body Scan Meditation</h3>
              <p className="text-muted-foreground mb-6">
                Systematically relax your entire body, releasing tension from head to toe
              </p>

              <Button
                onClick={isScanning ? pauseScan : startBodyScan}
                className="w-full h-14 text-lg mb-6 bg-adult-accent hover:bg-adult-accent/90"
              >
                {isScanning ? (
                  <>
                    <Pause className="mr-2 h-5 w-5" />
                    Pause Body Scan
                  </>
                ) : (
                  <>
                    <Play className="mr-2 h-5 w-5" />
                    {scanProgress > 0 ? "Resume" : "▶️ Start"} Body Scan
                  </>
                )}
              </Button>

              {scanProgress > 0 && (
                <div className="space-y-4">
                  <Progress value={scanProgress} className="h-2" />
                  
                  <Card className="p-6 bg-card text-center">
                    <div className="text-4xl mb-3">🧘</div>
                    <p className="text-lg font-semibold mb-2">
                      Focus on your{" "}
                      <span className="text-adult-accent">{bodyParts[currentPart]}</span>
                    </p>
                    <p className="text-muted-foreground text-sm">
                      {Math.floor((15 * (100 - scanProgress)) / 100)}:
                      {Math.floor(((15 * 60 * (100 - scanProgress)) / 100) % 60)
                        .toString()
                        .padStart(2, "0")}{" "}
                      remaining
                    </p>
                  </Card>

                  <div className="flex items-center justify-center">
                    <div className="w-24 h-24 rounded-full bg-primary/20 animate-pulse-soft flex items-center justify-center">
                      <div className="w-16 h-16 rounded-full bg-primary/40"></div>
                    </div>
                  </div>
                </div>
              )}
            </Card>

            {scanProgress === 100 && (
              <Button
                onClick={onClose}
                variant="outline"
                className="w-full h-12"
              >
                <CheckCircle2 className="mr-2 h-5 w-5" />
                ✅ Complete Session
              </Button>
            )}
          </TabsContent>

          <TabsContent value="journal" className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-3">Current stressors</h3>
              <div className="flex flex-wrap gap-2 mb-4">
                {["Career", "Health", "Finances", "Relationships", "Future", "World Events"].map(
                  (trigger) => (
                    <Badge
                      key={trigger}
                      variant="outline"
                      className="cursor-pointer px-4 py-2"
                    >
                      {trigger}
                    </Badge>
                  )
                )}
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-3">Reflection</h3>
              <Textarea
                placeholder="What's on your mind? What are you grateful for today?"
                className="min-h-32 mb-4"
              />
            </div>

            <Button className="w-full h-12 bg-adult-accent hover:bg-adult-accent/90">
              💾 Save Entry
            </Button>
          </TabsContent>
        </Tabs>
      </div>
    </Card>
  );
};

export default AdultIntervention;
