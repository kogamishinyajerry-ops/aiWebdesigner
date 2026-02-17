'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { AppLayout } from '@/components/layout/app-layout'

const presets = [
  { name: 'Hero Banner', prompt: '现代科技风格hero banner,渐变背景,抽象几何图形' },
  { name: '产品展示', prompt: '极简产品展示页面,白色背景,高质感' },
  { name: '登录页', prompt: '登录页面背景,磨砂玻璃效果,优雅渐变' },
  { name: '数据可视化', prompt: '仪表板背景,深色模式,科技感' },
]

export default function ImageGeneratorPage() {
  const [prompt, setPrompt] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedImage, setGeneratedImage] = useState<string | null>(null)

  const handleGenerate = async () => {
    if (!prompt.trim()) return

    setIsGenerating(true)
    try {
      // TODO: 调用后端API
      // const response = await fetch('/api/v1/generate/image', { ... })
      await new Promise(resolve => setTimeout(resolve, 2000))
      setGeneratedImage('/placeholder-generated.png')
    } catch (error) {
      console.error('生成失败:', error)
    } finally {
      setIsGenerating(false)
    }
  }

  const handlePresetClick = (presetPrompt: string) => {
    setPrompt(presetPrompt)
  }

  return (
    <AppLayout>
      <div className="space-y-6 animate-in">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
            图像生成器
          </h1>
          <p className="text-muted-foreground mt-2">
            使用AI生成高质量的网页图像素材
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Panel - Input */}
          <div className="lg:col-span-1 space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>输入描述</CardTitle>
                <CardDescription>
                  描述您想要生成的图像
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium mb-2 block">
                    提示词
                  </label>
                  <textarea
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="例如: 现代科技风格hero banner,渐变背景,抽象几何图形..."
                    className="w-full h-32 px-3 py-2 text-sm rounded-md border border-input bg-background focus:outline-none focus:ring-2 focus:ring-ring resize-none"
                  />
                </div>

                <div>
                  <label className="text-sm font-medium mb-2 block">
                    快捷预设
                  </label>
                  <div className="grid grid-cols-2 gap-2">
                    {presets.map((preset) => (
                      <Button
                        key={preset.name}
                        variant="outline"
                        size="sm"
                        className="h-auto py-2 px-3 text-xs justify-start"
                        onClick={() => handlePresetClick(preset.prompt)}
                      >
                        {preset.name}
                      </Button>
                    ))}
                  </div>
                </div>

                <Button
                  onClick={handleGenerate}
                  disabled={!prompt.trim() || isGenerating}
                  variant="gradient"
                  className="w-full"
                >
                  {isGenerating ? '生成中...' : '生成图像'}
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>生成设置</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium mb-2 block">
                    图像尺寸
                  </label>
                  <select className="w-full px-3 py-2 text-sm rounded-md border border-input bg-background">
                    <option>1920 x 1080 (16:9)</option>
                    <option>1280 x 720 (16:9)</option>
                    <option>1080 x 1080 (1:1)</option>
                    <option>800 x 600 (4:3)</option>
                  </select>
                </div>

                <div>
                  <label className="text-sm font-medium mb-2 block">
                    风格
                  </label>
                  <select className="w-full px-3 py-2 text-sm rounded-md border border-input bg-background">
                    <option>现代简约</option>
                    <option>科技感</option>
                    <option>优雅精致</option>
                    <option>活泼活泼</option>
                  </select>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Right Panel - Preview */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>生成预览</CardTitle>
                    <CardDescription>
                      生成的图像将显示在这里
                    </CardDescription>
                  </div>
                  {generatedImage && (
                    <div className="flex gap-2">
                      <Badge variant="secondary">1920x1080</Badge>
                      <Badge variant="outline">PNG</Badge>
                    </div>
                  )}
                </div>
              </CardHeader>
              <CardContent>
                <div className="aspect-video rounded-lg border-2 border-dashed border-muted-foreground/25 flex items-center justify-center bg-muted/50">
                  {isGenerating ? (
                    <div className="w-full space-y-3">
                      <Skeleton className="h-64 w-full" />
                      <div className="flex gap-2">
                        <Skeleton className="h-4 w-24" />
                        <Skeleton className="h-4 w-32" />
                      </div>
                    </div>
                  ) : generatedImage ? (
                    <div className="w-full h-full flex flex-col items-center justify-center space-y-4">
                      <div className="text-6xl">🎨</div>
                      <p className="text-muted-foreground">图像生成成功!</p>
                      <div className="flex gap-2">
                        <Button variant="outline" size="sm">
                          下载
                        </Button>
                        <Button variant="outline" size="sm">
                          复制链接
                        </Button>
                      </div>
                    </div>
                  ) : (
                    <div className="text-center space-y-4">
                      <div className="text-6xl opacity-50">🖼️</div>
                      <div>
                        <p className="text-sm text-muted-foreground mb-2">
                          在左侧输入描述并点击生成
                        </p>
                        <p className="text-xs text-muted-foreground">
                          支持多种风格和尺寸
                        </p>
                      </div>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </AppLayout>
  )
}
