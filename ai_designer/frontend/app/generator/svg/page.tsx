'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { apiService } from '@/lib/api-service'
import { ArrowLeft } from 'lucide-react'
import Link from 'next/link'

const svgPresets = [
  { name: 'Logo图标', prompt: '现代简约logo图标,几何形状,扁平化设计' },
  { name: '背景图案', prompt: '网页背景图案,抽象几何,重复纹理' },
  { name: '插画元素', prompt: '扁平化插画元素,人物图标,简洁风格' },
  { name: '数据图表', prompt: '数据可视化图表,柱状图,折线图' },
]

const styles = [
  { id: 'minimal', name: '简约风格' },
  { id: 'modern', name: '现代风格' },
  { id: 'playful', name: '活泼风格' },
  { id: 'geometric', name: '几何风格' },
]

export default function SVGGeneratorPage() {
  const [prompt, setPrompt] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedSVG, setGeneratedSVG] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [selectedStyle, setSelectedStyle] = useState('minimal')
  const [color, setColor] = useState('#6366f1')

  const handleGenerate = async () => {
    if (!prompt.trim()) return

    setIsGenerating(true)
    setError(null)
    try {
      const response = await apiService.generateSVG({
        prompt: prompt.trim(),
        style: selectedStyle,
        color_palette: [color],
        width: 512,
        height: 512,
      })

      if (response.success && response.svg_code) {
        setGeneratedSVG(response.svg_code)
      } else {
        throw new Error('生成失败')
      }
    } catch (error) {
      console.error('SVG生成失败:', error)
      setError(error instanceof Error ? error.message : '生成失败，请重试')
    } finally {
      setIsGenerating(false)
    }
  }

  const handlePresetClick = (presetPrompt: string) => {
    setPrompt(presetPrompt)
  }

  const handleDownload = () => {
    if (!generatedSVG) return
    const blob = new Blob([generatedSVG], { type: 'image/svg+xml' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `ai-generated-svg-${Date.now()}.svg`
    link.click()
    URL.revokeObjectURL(url)
  }

  const handleCopy = () => {
    if (!generatedSVG) return
    navigator.clipboard.writeText(generatedSVG)
  }

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="container mx-auto space-y-6 animate-in">
        {/* Back Button */}
        <Link href="/">
          <Button variant="ghost" className="mb-4">
            <ArrowLeft className="w-4 h-4 mr-2" />
            返回首页
          </Button>
        </Link>

        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
            SVG 生成器
          </h1>
          <p className="text-muted-foreground mt-2">
            使用AI生成可缩放的矢量图形
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Panel - Input */}
          <div className="lg:col-span-1 space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>输入描述</CardTitle>
                <CardDescription>
                  描述您想要生成的SVG图形
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
                    placeholder="例如: 现代简约logo图标,几何形状,扁平化设计..."
                    className="w-full h-32 px-3 py-2 text-sm rounded-md border border-input bg-background focus:outline-none focus:ring-2 focus:ring-ring resize-none"
                  />
                </div>

                <div>
                  <label className="text-sm font-medium mb-2 block">
                    快捷预设
                  </label>
                  <div className="grid grid-cols-2 gap-2">
                    {svgPresets.map((preset) => (
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
                  {isGenerating ? '生成中...' : '生成SVG'}
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>样式设置</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium mb-2 block">
                    风格
                  </label>
                  <select
                    value={selectedStyle}
                    onChange={(e) => setSelectedStyle(e.target.value)}
                    className="w-full px-3 py-2 text-sm rounded-md border border-input bg-background"
                  >
                    {styles.map((style) => (
                      <option key={style.id} value={style.id}>
                        {style.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="text-sm font-medium mb-2 block">
                    主色调
                  </label>
                  <div className="flex gap-2 items-center">
                    <input
                      type="color"
                      value={color}
                      onChange={(e) => setColor(e.target.value)}
                      className="w-10 h-10 rounded border cursor-pointer"
                    />
                    <span className="text-sm text-muted-foreground">{color}</span>
                  </div>
                </div>

                {error && (
                  <div className="p-3 bg-destructive/10 border border-destructive/20 rounded-md">
                    <p className="text-sm text-destructive">{error}</p>
                  </div>
                )}
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
                      生成的SVG将显示在这里
                    </CardDescription>
                  </div>
                  {generatedSVG && (
                    <div className="flex gap-2">
                      <Badge variant="secondary">SVG</Badge>
                      <Badge variant="outline">矢量图形</Badge>
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
                  ) : generatedSVG ? (
                    <div className="w-full h-full flex flex-col items-center justify-center space-y-4">
                      <div
                        dangerouslySetInnerHTML={{ __html: generatedSVG }}
                        className="max-w-full max-h-full"
                      />
                      <div className="flex gap-2">
                        <Button onClick={handleDownload} variant="outline" size="sm">
                          下载SVG
                        </Button>
                        <Button onClick={handleCopy} variant="outline" size="sm">
                          复制代码
                        </Button>
                        <Button
                          onClick={() => setGeneratedSVG(null)}
                          variant="outline"
                          size="sm"
                        >
                          清除
                        </Button>
                      </div>
                    </div>
                  ) : (
                    <div className="text-center space-y-4">
                      <div className="text-6xl opacity-50">📐</div>
                      <div>
                        <p className="text-sm text-muted-foreground mb-2">
                          在左侧输入描述并点击生成
                        </p>
                        <p className="text-xs text-muted-foreground">
                          生成的SVG可无限缩放，适用于任何尺寸
                        </p>
                      </div>
                    </div>
                  )}
                </div>

                {generatedSVG && (
                  <div className="mt-4">
                    <h4 className="text-sm font-medium mb-2">SVG 代码</h4>
                    <div className="bg-muted p-3 rounded-md">
                      <pre className="text-xs overflow-x-auto">
                        {generatedSVG}
                      </pre>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
