import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Phone, MessageSquare, Globe, Wind, Droplet, Footprints } from "lucide-react";

interface CrisisModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onContinue: () => void;
  onStop: () => void;
}

const CrisisModal = ({ open, onOpenChange, onContinue, onStop }: CrisisModalProps) => {
  const [showTechnique, setShowTechnique] = useState<string | null>(null);

  const techniques = {
    breathing: {
      icon: <Wind className="h-12 w-12" />,
      title: "Box Breathing (30 seconds)",
      instructions: [
        "Breathe in for 4 counts",
        "Hold for 4 counts",
        "Breathe out for 4 counts",
        "Hold for 4 counts",
        "Repeat 3 times"
      ]
    },
    cold: {
      icon: <Droplet className="h-12 w-12" />,
      title: "Cold Water Face Dunk",
      instructions: [
        "Fill a bowl with cold water and ice",
        "Hold your breath",
        "Dunk your face for 15-30 seconds",
        "This activates the dive reflex, instantly calming your nervous system"
      ]
    },
    movement: {
      icon: <Footprints className="h-12 w-12" />,
      title: "Movement Break",
      instructions: [
        "Stand up and shake out your hands",
        "Roll your shoulders back 5 times",
        "Take 5 steps forward and 5 back",
        "Jump up and down 5 times",
        "Movement helps release stress hormones"
      ]
    }
  };

  if (showTechnique) {
    const technique = techniques[showTechnique as keyof typeof techniques];
    return (
      <Dialog open={open} onOpenChange={onOpenChange}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <div className="flex items-center gap-3 mb-2">
              <div className="text-primary">{technique.icon}</div>
              <DialogTitle className="text-2xl">{technique.title}</DialogTitle>
            </div>
          </DialogHeader>
          
          <Card className="p-6 bg-muted">
            <ol className="space-y-3">
              {technique.instructions.map((instruction, i) => (
                <li key={i} className="flex items-start gap-3">
                  <span className="flex-shrink-0 w-6 h-6 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-sm font-semibold">
                    {i + 1}
                  </span>
                  <span className="text-lg">{instruction}</span>
                </li>
              ))}
            </ol>
          </Card>

          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setShowTechnique(null)}
              className="w-full"
            >
              Back to Resources
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    );
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <div className="flex items-center gap-3 mb-2">
            <span className="text-5xl">🚨</span>
            <div>
              <DialogTitle className="text-2xl border-t-4 border-t-destructive pt-1">
                Very High Stress Detected
              </DialogTitle>
              <DialogDescription className="text-base mt-2">
                Your wellbeing matters. Let's get you help.
              </DialogDescription>
            </div>
          </div>
        </DialogHeader>

        {/* Crisis Resources */}
        <Card className="p-6 bg-destructive/10 border-destructive">
          <h3 className="text-xl font-semibold mb-4">
            If you're in crisis, reach out now:
          </h3>
          
          <div className="space-y-4">
            <Card className="p-4 hover:shadow-md transition-shadow cursor-pointer">
              <div className="flex items-center gap-4">
                <Phone className="h-8 w-8 text-destructive" />
                <div className="flex-1">
                  <h4 className="font-semibold text-lg">988 Suicide & Crisis Lifeline</h4>
                  <p className="text-muted-foreground">24/7 support in English and Spanish</p>
                </div>
                <Button size="lg" className="bg-destructive hover:bg-destructive/90">
                  Call 988
                </Button>
              </div>
            </Card>

            <Card className="p-4 hover:shadow-md transition-shadow cursor-pointer">
              <div className="flex items-center gap-4">
                <MessageSquare className="h-8 w-8 text-primary" />
                <div className="flex-1">
                  <h4 className="font-semibold text-lg">Crisis Text Line</h4>
                  <p className="text-muted-foreground">Text with a trained crisis counselor</p>
                </div>
                <Button size="lg" variant="outline">
                  Text HOME to 741741
                </Button>
              </div>
            </Card>

            <Card className="p-4 hover:shadow-md transition-shadow cursor-pointer">
              <div className="flex items-center gap-4">
                <Globe className="h-8 w-8 text-secondary" />
                <div className="flex-1">
                  <h4 className="font-semibold text-lg">International Resources</h4>
                  <p className="text-muted-foreground">Find helplines worldwide</p>
                </div>
                <Button size="lg" variant="outline">
                  Visit findahelpline.com
                </Button>
              </div>
            </Card>
          </div>
        </Card>

        {/* Immediate Calming */}
        <div>
          <h3 className="text-xl font-semibold mb-4">Quick Calming Techniques:</h3>
          <div className="grid grid-cols-3 gap-3">
            <Button
              variant="outline"
              className="h-auto py-6 flex flex-col gap-2"
              onClick={() => setShowTechnique("breathing")}
            >
              <Wind className="h-8 w-8 text-primary" />
              <span className="text-sm font-semibold">Box Breathing</span>
              <span className="text-xs text-muted-foreground">30 sec</span>
            </Button>

            <Button
              variant="outline"
              className="h-auto py-6 flex flex-col gap-2"
              onClick={() => setShowTechnique("cold")}
            >
              <Droplet className="h-8 w-8 text-primary" />
              <span className="text-sm font-semibold">Cold Water</span>
              <span className="text-xs text-muted-foreground">Face dunk</span>
            </Button>

            <Button
              variant="outline"
              className="h-auto py-6 flex flex-col gap-2"
              onClick={() => setShowTechnique("movement")}
            >
              <Footprints className="h-8 w-8 text-primary" />
              <span className="text-sm font-semibold">Movement</span>
              <span className="text-xs text-muted-foreground">Break</span>
            </Button>
          </div>
        </div>

        {/* Professional Help */}
        <Card className="p-4 bg-muted">
          <p className="text-sm text-muted-foreground mb-2">
            Consider speaking with a mental health professional
          </p>
          <Button variant="link" className="p-0 h-auto text-primary">
            Find a therapist →
          </Button>
        </Card>

        <DialogFooter className="flex-col sm:flex-col gap-2">
          <Button
            onClick={onContinue}
            className="w-full h-12 bg-calm hover:bg-calm/90"
          >
            I'm safe, continue monitoring
          </Button>
          <Button
            onClick={onStop}
            variant="outline"
            className="w-full h-12"
          >
            Stop session
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default CrisisModal;
