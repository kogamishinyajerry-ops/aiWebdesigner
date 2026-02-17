import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Sparkles, Image, Code2, Palette, Zap, Rocket } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted">
      {/* Hero Section */}
      <section className="container px-4 py-20 mx-auto">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          <Badge variant="secondary" className="mb-4">
            <Sparkles className="w-4 h-4 mr-2" />
            AI驱动的艺术级设计
          </Badge>
          
          <h1 className="text-6xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-primary via-purple-500 to-pink-500 animate-in">
            AI Designer
          </h1>
          
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            以Gemini为标杆，打造具备极致艺术美学的AI前端设计系统
          </p>
          
          <div className="flex gap-4 justify-center">
            <Button size="lg" className="text-lg">
              <Rocket className="w-5 h-5 mr-2" />
              开始创作
            </Button>
            <Button size="lg" variant="outline">
              了解更多
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container px-4 py-16 mx-auto">
        <h2 className="text-3xl font-bold text-center mb-12">
          核心功能
        </h2>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <Image className="w-12 h-12 text-primary mb-4" />
              <CardTitle>图像生成</CardTitle>
              <CardDescription>
                AI驱动的Hero Banner、Icon集、背景纹理生成
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <Palette className="w-12 h-12 text-primary mb-4" />
              <CardTitle>矢量设计</CardTitle>
              <CardDescription>
                文本描述生成SVG，草图转矢量，批量风格化
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <Code2 className="w-12 h-12 text-primary mb-4" />
              <CardTitle>代码生成</CardTitle>
              <CardDescription>
                艺术级设计到优雅代码，Tailwind CSS智能生成
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <Sparkles className="w-12 h-12 text-primary mb-4" />
              <CardTitle>美学引擎</CardTitle>
              <CardDescription>
                风格识别、色彩推荐、布局优化、审美评分
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </section>

      {/* Tech Stack Section */}
      <section className="container px-4 py-16 mx-auto">
        <h2 className="text-3xl font-bold text-center mb-12">
          技术栈
        </h2>
        
        <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">前端</CardTitle>
              <CardContent className="pt-4 space-y-2">
                <Badge variant="outline">Next.js 14</Badge>
                <Badge variant="outline">React</Badge>
                <Badge variant="outline">Tailwind CSS</Badge>
                <Badge variant="outline">TypeScript</Badge>
              </CardContent>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-lg">后端</CardTitle>
              <CardContent className="pt-4 space-y-2">
                <Badge variant="outline">FastAPI</Badge>
                <Badge variant="outline">Python</Badge>
                <Badge variant="outline">PostgreSQL</Badge>
                <Badge variant="outline">Redis</Badge>
              </CardContent>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-lg">AI模型</CardTitle>
              <CardContent className="pt-4 space-y-2">
                <Badge variant="outline">FLUX.1</Badge>
                <Badge variant="outline">Gemini API</Badge>
                <Badge variant="outline">CLIP</Badge>
                <Badge variant="outline">GPT-4o</Badge>
              </CardContent>
            </CardHeader>
          </Card>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container px-4 py-20 mx-auto">
        <Card className="max-w-2xl mx-auto border-2 border-primary/20">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl mb-4">
              <Zap className="w-8 h-8 inline-block mr-2" />
              立即开始
            </CardTitle>
            <CardDescription className="text-base">
              开发中...预计4周后发布MVP版本
            </CardDescription>
          </CardHeader>
          <CardContent className="flex justify-center gap-4">
            <Button size="lg">
              查看开发计划
            </Button>
            <Button size="lg" variant="outline">
              GitHub
            </Button>
          </CardContent>
        </Card>
      </section>
    </div>
  )
}
