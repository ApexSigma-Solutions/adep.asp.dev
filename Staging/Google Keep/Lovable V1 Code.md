

import { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { useToast } from "@/hooks/use-toast";
import { 
  Crown, 
  DollarSign, 
  Download, 
  TrendingUp, 
  Users, 
  BookOpen,
  Shield,
  Sparkles,
  Mail,
  Star,
  CheckCircle
} from 'lucide-react';

const Index = () => {
  const [email, setEmail] = useState('');
  const { toast } = useToast();

  const handleNewsletterSignup = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) {
      toast({
        title: "Please enter your email",
        description: "We need your email to send you valuable budgeting tips!",
        variant: "destructive",
      });
      return;
    }
    
    toast({
      title: "Welcome to the Royal Family! 👑",
      description: "You've successfully joined SA Budget Queen. Get ready for amazing budgeting tips!",
    });
    setEmail('');
  };

  const budgetTemplates = [
    { name: "Monthly Household Budget", description: "Complete family budget planner", downloads: "2,341" },
    { name: "Grocery Shopping Tracker", description: "Smart shopping list with price comparison", downloads: "1,892" },
    { name: "Debt Elimination Plan", description: "Step-by-step debt freedom roadmap", downloads: "1,567" },
    { name: "Emergency Fund Builder", description: "Build your financial safety net", downloads: "1,234" },
  ];

  const educationalTips = [
    {
      title: "Smart Grocery Shopping in SA",
      description: "Learn how to cut your grocery bill by 30% with these proven South African shopping strategies.",
      category: "Shopping"
    },
    {
      title: "Understanding Bank Fees",
      description: "Navigate SA banking fees and find the most cost-effective banking solutions for your family.",
      category: "Banking"
    },
    {
      title: "Building Your Emergency Fund",
      description: "Start small and build big - practical steps to create financial security in tough times.",
      category: "Savings"
    },
    {
      title: "Subscription Audit Guide",
      description: "Identify and eliminate unnecessary subscriptions bleeding your budget dry.",
      category: "Subscriptions"
    }
  ];

  const testimonials = [
    {
      name: "Thandi M.",
      location: "Cape Town",
      text: "SA Budget Queen helped me save R2,500 per month! The grocery shopping tips alone paid for themselves.",
      rating: 5
    },
    {
      name: "Johan & Maria V.",
      location: "Johannesburg",
      text: "Finally found budgeting advice that works for SA families. We're debt-free thanks to the debt elimination plan!",
      rating: 5
    },
    {
      name: "Nomsa K.",
      location: "Durban",
      text: "The subscription tracker found R800 in forgotten subscriptions I was still paying for. Life-changing!",
      rating: 5
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-50 to-white">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <Crown className="h-8 w-8 text-purple-600" />
              <span className="text-2xl font-bold text-gray-900">SA Budget Queen</span>
            </div>
            <div className="hidden md:flex space-x-8">
              <a href="#education className="text-gray-700 hover:text-purple-600 transition-colors">Learn</a>
              <a href="#templates className="text-gray-700 hover:text-purple-600 transition-colors">Templates</a>
              <a href="#community className="text-gray-700 hover:text-purple-600 transition-colors">Community</a>
              <Button className="bg-purple-600 hover:bg-purple-700">
                <Crown className="w-4 h-4 mr-2" />
                Join Premium
              </Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center">
            <div className="flex justify-center mb-6">
              <div className="relative">
                <Crown className="h-20 w-20 text-purple-600" />
                <Sparkles className="h-6 w-6 text-yellow-500 absolute -top-2 -right-2 animate-pulse" />
              </div>
            </div>
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              Live Like <span className="text-purple-600">Royalty</span>
              <br />
              on Any Budget
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Join thousands of South African families learning to manage their money like royalty. 
              Smart budgeting, smarter shopping, financial freedom.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-4 text-lg">
                <BookOpen className="w-5 h-5 mr-2" />
                Start Learning Free
              </Button>
              <Button size="lg" variant="outline" className="border-purple-600 text-purple-600 hover:bg-purple-50 px-8 py-4 text-lg">
                <Download className="w-5 h-5 mr-2" />
                Download Templates
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
            <div className="space-y-2">
              <div className="text-3xl font-bold text-purple-600">25,000+</div>
              <div className="text-gray-600">Families Helped</div>
            </div>
            <div className="space-y-2">
              <div className="text-3xl font-bold text-purple-600">R2.8M</div>
              <div className="text-gray-600">Money Saved</div>
            </div>
            <div className="space-y-2">
              <div className="text-3xl font-bold text-purple-600">87%</div>
              <div className="text-gray-600">Reduce Monthly Expenses</div>
            </div>
            <div className="space-y-2">
              <div className="text-3xl font-bold text-purple-600">4.9★</div>
              <div className="text-gray-600">Community Rating</div>
            </div>
          </div>
        </div>
      </section>

      {/* Educational Content Section */}
      <section id="education" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Royal Financial Education
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Learn from South Africa's most practical budgeting experts. Real strategies for real families.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {educationalTips.map((tip, index) => (
              <Card key={index} className="hover:shadow-lg transition-shadow cursor-pointer group">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <Badge variant="secondary" className="bg-purple-100 text-purple-700">
                      {tip.category}
                    </Badge>
                    <BookOpen className="w-5 h-5 text-purple-600 group-hover:text-purple-800 transition-colors" />
                  </div>
                  <CardTitle className="text-xl group-hover:text-purple-600 transition-colors">
                    {tip.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">
                    {tip.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Budget Templates Section */}
      <section id="templates" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Free Budget Templates
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Professional spreadsheet templates used by thousands of SA families to take control of their finances.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {budgetTemplates.map((template, index) => (
              <Card key={index} className="hover:shadow-lg transition-shadow group">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <DollarSign className="w-5 h-5 text-green-600" />
                      <Badge variant="outline" className="text-xs">
                        {template.downloads} downloads
                      </Badge>
                    </div>
                    <Download className="w-5 h-5 text-gray-400 group-hover:text-purple-600 transition-colors" />
                  </div>
                  <CardTitle className="text-xl">{template.name}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base mb-4">
                    {template.description}
                  </CardDescription>
                  <Button className="w-full bg-purple-600 hover:bg-purple-700">
                    <Download className="w-4 h-4 mr-2" />
                    Download Free
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Community Testimonials */}
      <section id="community" className="py-20 bg-gradient-to-r from-purple-600 to-purple-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Royal Success Stories
            </h2>
            <p className="text-xl text-purple-100 max-w-2xl mx-auto">
              Real families, real results. Join the Budget Queen community today.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <Card key={index} className="bg-white/10 backdrop-blur-sm border-white/20 text-white">
                <CardHeader>
                  <div className="flex items-center space-x-1 mb-2">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                    ))}
                  </div>
                  <CardTitle className="text-lg">
                    {testimonial.name}
                  </CardTitle>
                  <CardDescription className="text-purple-100">
                    {testimonial.location}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-white/90">"{testimonial.text}"</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Premium Preview */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Coming Soon: Premium App Features
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              The ultimate budgeting companion that connects to your bank accounts and automatically 
              tracks spending, finds forgotten subscriptions, and optimizes your expenses.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="text-center p-6 border-2 border-purple-200 hover:border-purple-400 transition-colors">
              <Shield className="w-12 h-12 text-purple-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">Bank Integration</h3>
              <p className="text-gray-600">Securely connect your SA bank accounts for automatic expense tracking</p>
            </Card>
            <Card className="text-center p-6 border-2 border-purple-200 hover:border-purple-400 transition-colors">
              <TrendingUp className="w-12 h-12 text-purple-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">Smart Analysis</h3>
              <p className="text-gray-600">AI-powered insights to identify saving opportunities and spending patterns</p>
            </Card>
            <Card className="text-center p-6 border-2 border-purple-200 hover:border-purple-400 transition-colors">
              <CheckCircle className="w-12 h-12 text-purple-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">Subscription Scanner</h3>
              <p className="text-gray-600">Find forgotten subscriptions and discover cheaper alternatives</p>
            </Card>
          </div>
          
          <div className="text-center mt-12">
            <Button size="lg" className="bg-purple-600 hover:bg-purple-700 px-8 py-4 text-lg">
              <Crown className="w-5 h-5 mr-2" />
              Join the Waitlist
            </Button>
          </div>
        </div>
      </section>

      {/* Newsletter Signup */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-2xl shadow-xl p-8 md:p-12">
            <Crown className="w-16 h-16 text-purple-600 mx-auto mb-6" />
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Join the Royal Family
            </h2>
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              Get exclusive budgeting tips, early access to new templates, and join a community 
              of South Africans committed to financial freedom.
            </p>
            
            <form onSubmit={handleNewsletterSignup} className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
              <Input
                type="email"
                placeholder="Enter your email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="flex-1 h-12 text-lg"
              />
              <Button type="submit" size="lg" className="bg-purple-600 hover:bg-purple-700 h-12 px-6">
                <Mail className="w-5 h-5 mr-2" />
                Join Now
              </Button>
            </form>
            
            <div className="flex items-center justify-center space-x-6 mt-8 text-sm text-gray-500">
              <div className="flex items-center">
                <Users className="w-4 h-4 mr-1" />
                25,000+ members
              </div>
              <div className="flex items-center">
                <Shield className="w-4 h-4 mr-1" />
                100% free
              </div>
              <div className="flex items-center">
                <Mail className="w-4 h-4 mr-1" />
                No spam, ever
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="col-span-1 md:col-span-2">
              <div className="flex items-center space-x-2 mb-4">
                <Crown className="h-8 w-8 text-purple-400" />
                <span className="text-2xl font-bold">SA Budget Queen</span>
              </div>
              <p className="text-gray-400 max-w-md">
                Empowering South African families to achieve financial freedom through smart budgeting, 
                practical education, and community support.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Learn</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="# className="hover:text-white transition-colors">Budgeting Basics</a></li>
                <li><a href="# className="hover:text-white transition-colors">Smart Shopping</a></li>
                <li><a href="# className="hover:text-white transition-colors">Debt Freedom</a></li>
                <li><a href="# className="hover:text-white transition-colors">Emergency Funds</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Community</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="# className="hover:text-white transition-colors">Success Stories</a></li>
                <li><a href="# className="hover:text-white transition-colors">Support Forum</a></li>
                <li><a href="# className="hover:text-white transition-colors">Newsletter</a></li>
                <li><a href="# className="hover:text-white transition-colors">Contact Us</a></li>
              </ul>
            </div>
          </div>
          
          <Separator className="my-8 bg-gray-800" />
          
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400 text-sm">
              © 2024 SA Budget Queen. All rights reserved. Made with ❤️ for South African families.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <a href="# className="text-gray-400 hover:text-white transition-colors text-sm">Privacy Policy</a>
              <a href="# className="text-gray-400 hover:text-white transition-colors text-sm">Terms of Service</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
