'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { apiService } from '@/lib/api-service'

// 艺术风格类型
const ART_STYLES = [
  { value: 'van_gogh', name: '梵高', description: '星空风格，旋涡笔触，浓烈色彩' },
  { value: 'picasso', name: '毕加索', description: '立体主义，几何碎片，多视角' },
  { value: 'dali', name: '达利', description: '超现实主义，梦境，融化的时钟' },
  { value: 'monet', name: '莫奈', description: '印象派，光影色彩，自然和谐' },
  { value: 'kandinsky', name: '康定斯基', description: '抽象艺术，几何形状，色彩音乐' },
  { value: 'klee', name: '克利', description: '几何抽象，童趣，简约美学' },
  { value: 'matisse', name: '马蒂斯', description: '剪纸风格，大胆色块，有机曲线' },
  { value: 'warhol', name: '沃霍尔', description: '波普艺术，重复图像，鲜艳色彩' },
  { value: 'escher', name: '埃舍尔', description: '视错觉，无限循环，不可能图形' },
  { value: 'hiroshige', name: '歌川广重', description: '浮世绘，日式风格，留白意境' },
]

// UI组件类型
const UI_COMPONENTS = [
  { value: 'hero_banner', name: 'Hero Banner', description: '主横幅' },
  { value: 'header', name: 'Header', description: '顶部导航' },
  { value: 'sidebar', name: 'Sidebar', description: '侧边栏' },
  { value: 'card', name: 'Card', description: '卡片' },
  { value: 'button', name: 'Button', description: '按钮' },
  { value: 'background', name: 'Background', description: '背景' },
  { value: 'modal', name: 'Modal', description: '模态框' },
  { value: 'form_input', name: 'Form Input', description: '表单输入' },
]

export default function AestheticPage() {
  const [selectedStyle, setSelectedStyle] = useState('van_gogh')
  const [pageDescription, setPageDescription] = useState('')
  const [selectedComponents, setSelectedComponents] = useState<string[]>(['hero_banner', 'card', 'button'])
  const [colorPreference, setColorPreference] = useState('')
  const [mood, setMood] = useState('')
  const [complexity, setComplexity] = useState('medium')
  const [includeInteractions, setIncludeInteractions] = useState(true)
  const [includeAssets, setIncludeAssets] = useState(true)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [activeTab, setActiveTab] = useState('summary')

  const handleGenerate = async () => {
    if (!pageDescription.trim()) {
      alert('请输入页面描述')
      return
    }

    setLoading(true)
    setResult(null)

    try {
      const response = await apiService.generateAestheticDesign({
        art_style: selectedStyle,
        page_description: pageDescription,
        target_components: selectedComponents,
        color_preference: colorPreference || undefined,
        mood: mood || undefined,
        complexity,
        include_interactions: includeInteractions,
        include_assets: includeAssets,
      })

      setResult(response)
      setActiveTab('summary')
    } catch (error: any) {
      console.error('生成失败:', error)
      alert('生成失败: ' + (error.message || '未知错误'))
    } finally {
      setLoading(false)
    }
  }

  const toggleComponent = (component: string) => {
    setSelectedComponents(prev =>
      prev.includes(component)
        ? prev.filter(c => c !== component)
        : [...prev, component]
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-8">
      {/* Header */}
      <div className="max-w-7xl mx-auto mb-8">
        <Button
          variant="ghost"
          onClick={() => window.location.href = '/'}
          className="mb-6"
        >
          ← 返回首页
        </Button>

        <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-2">
          🎨 AI美学设计引擎
        </h1>
        <p className="text-gray-600 text-lg">
          参考艺术巨匠的作品风格，为你生成极致美感的前端界面设计方案
        </p>
      </div>

      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* 左侧：输入区域 */}
        <Card className="p-6 bg-white/80 backdrop-blur-sm shadow-xl">
          <h2 className="text-2xl font-semibold mb-6 text-gray-800">设计参数</h2>

          {/* 艺术风格选择 */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-3">
              选择艺术风格
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {ART_STYLES.map((style) => (
                <button
                  key={style.value}
                  onClick={() => setSelectedStyle(style.value)}
                  className={`p-4 rounded-xl border-2 text-left transition-all ${
                    selectedStyle === style.value
                      ? 'border-purple-500 bg-purple-50 ring-2 ring-purple-200'
                      : 'border-gray-200 hover:border-gray-300 bg-white'
                  }`}
                >
                  <div className="font-semibold text-gray-900 mb-1">
                    {style.name}
                  </div>
                  <div className="text-xs text-gray-600">
                    {style.description}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* 页面描述 */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              页面描述 *
            </label>
            <textarea
              value={pageDescription}
              onChange={(e) => setPageDescription(e.target.value)}
              placeholder="描述你的页面：例如，一个AI图像生成应用，包含输入区域、预览区域和生成按钮..."
              className="w-full p-4 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition-all resize-none"
              rows={4}
            />
          </div>

          {/* 组件选择 */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-3">
              选择要设计的组件
            </label>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
              {UI_COMPONENTS.map((component) => (
                <button
                  key={component.value}
                  onClick={() => toggleComponent(component.value)}
                  className={`p-3 rounded-lg border text-sm transition-all ${
                    selectedComponents.includes(component.value)
                      ? 'border-purple-500 bg-purple-50 text-purple-700'
                      : 'border-gray-200 hover:border-gray-300 text-gray-600'
                  }`}
                >
                  {component.name}
                </button>
              ))}
            </div>
          </div>

          {/* 颜色偏好 */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              颜色偏好（可选）
            </label>
            <input
              type="text"
              value={colorPreference}
              onChange={(e) => setColorPreference(e.target.value)}
              placeholder="warm, cool, dark, light..."
              className="w-full p-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition-all"
            />
          </div>

          {/* 情感基调 */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              情感基调（可选）
            </label>
            <input
              type="text"
              value={mood}
              onChange={(e) => setMood(e.target.value)}
              placeholder="浪漫、科技感、温馨、严肃..."
              className="w-full p-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition-all"
            />
          </div>

          {/* 复杂度 */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-3">
              复杂度
            </label>
            <div className="flex gap-3">
              {['low', 'medium', 'high'].map((level) => (
                <button
                  key={level}
                  onClick={() => setComplexity(level)}
                  className={`flex-1 p-3 rounded-lg border capitalize transition-all ${
                    complexity === level
                      ? 'border-purple-500 bg-purple-50 text-purple-700'
                      : 'border-gray-200 hover:border-gray-300 text-gray-600'
                  }`}
                >
                  {level}
                </button>
              ))}
            </div>
          </div>

          {/* 选项开关 */}
          <div className="mb-6 space-y-3">
            <label className="flex items-center space-x-3 cursor-pointer">
              <input
                type="checkbox"
                checked={includeInteractions}
                onChange={(e) => setIncludeInteractions(e.target.checked)}
                className="w-5 h-5 text-purple-600 rounded focus:ring-purple-500"
              />
              <span className="text-gray-700">包含交互动效设计</span>
            </label>
            <label className="flex items-center space-x-3 cursor-pointer">
              <input
                type="checkbox"
                checked={includeAssets}
                onChange={(e) => setIncludeAssets(e.target.checked)}
                className="w-5 h-5 text-purple-600 rounded focus:ring-purple-500"
              />
              <span className="text-gray-700">生成视觉素材提示词</span>
            </label>
          </div>

          {/* 生成按钮 */}
          <Button
            onClick={handleGenerate}
            disabled={loading}
            className="w-full py-4 text-lg bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-xl shadow-lg transition-all disabled:opacity-50"
          >
            {loading ? '正在生成...' : '🎨 生成美学设计方案'}
          </Button>
        </Card>

        {/* 右侧：结果展示 */}
        <Card className="p-6 bg-white/80 backdrop-blur-sm shadow-xl">
          {result ? (
            <>
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-semibold text-gray-800">设计方案</h2>
                <span className="text-sm text-gray-500">
                  生成时间: {result.generation_time.toFixed(2)}s
                </span>
              </div>

              {/* 标签页 */}
              <div className="flex gap-2 mb-6 overflow-x-auto">
                {['summary', 'colors', 'components', 'interactions', 'assets'].map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`px-4 py-2 rounded-lg capitalize transition-all whitespace-nowrap ${
                      activeTab === tab
                        ? 'bg-purple-600 text-white'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                  >
                    {tab}
                  </button>
                ))}
              </div>

              {/* 内容区域 */}
              <div className="bg-gray-50 rounded-xl p-6 max-h-[600px] overflow-y-auto">
                {activeTab === 'summary' && (
                  <div className="prose prose-sm max-w-none">
                    <h3 className="text-xl font-bold mb-4">{result.aesthetic_analysis.style_name} 风格</h3>
                    <p className="text-gray-700 mb-4">{result.aesthetic_analysis.style_description}</p>
                    
                    <h4 className="font-semibold mb-2">关键特征</h4>
                    <ul className="list-disc pl-5 mb-4">
                      {result.aesthetic_analysis.key_characteristics.map((char: string, idx: number) => (
                        <li key={idx} className="text-gray-600">{char}</li>
                      ))}
                    </ul>

                    <h4 className="font-semibold mb-2">情感基调</h4>
                    <p className="text-gray-600">{result.aesthetic_analysis.mood}</p>

                    <div className="mt-6">
                      <h4 className="font-semibold mb-3">色彩预览</h4>
                      <div className="flex gap-2 flex-wrap">
                        {Object.values(result.global_color_palette).slice(0, 6).map((color: any, idx: number) => (
                          <div
                            key={idx}
                            className="w-16 h-16 rounded-lg shadow-md"
                            style={{ backgroundColor: color }}
                            title={color}
                          />
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'colors' && (
                  <div>
                    <h3 className="text-xl font-bold mb-4">色彩方案</h3>
                    <div className="space-y-3">
                      {Object.entries(result.global_color_palette).map(([key, value]: [string, any]) => (
                        <div key={key} className="flex items-center gap-4">
                          <div
                            className="w-20 h-20 rounded-lg shadow-md flex-shrink-0"
                            style={{ backgroundColor: value }}
                          />
                          <div>
                            <div className="font-semibold text-gray-900 capitalize">{key}</div>
                            <code className="text-sm text-gray-600">{value}</code>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {activeTab === 'components' && (
                  <div className="space-y-6">
                    {result.component_designs.map((design: any, idx: number) => (
                      <div key={idx} className="border-b border-gray-200 pb-4 last:border-0">
                        <h4 className="text-lg font-semibold text-gray-900 mb-2 capitalize">
                          {design.component}
                        </h4>
                        <p className="text-sm text-gray-600 mb-3">{design.layout_description}</p>
                        
                        <div className="bg-gray-100 rounded-lg p-3 mb-3">
                          <div className="text-xs font-semibold text-gray-500 mb-1">Tailwind Classes</div>
                          <code className="text-xs text-purple-700">{design.tailwind_classes}</code>
                        </div>

                        <div className="bg-gray-900 rounded-lg p-3 overflow-x-auto">
                          <div className="text-xs font-semibold text-gray-400 mb-1">CSS</div>
                          <pre className="text-xs text-green-400 whitespace-pre-wrap">{design.css_code}</pre>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {activeTab === 'interactions' && (
                  <div className="space-y-3">
                    {result.interactions.map((interaction: any, idx: number) => (
                      <div key={idx} className="bg-white rounded-lg p-4 border">
                        <div className="font-semibold text-gray-900 capitalize mb-1">
                          {interaction.component} - {interaction.interaction_type}
                        </div>
                        <div className="text-sm text-gray-600">{interaction.effect}</div>
                        <div className="text-xs text-gray-500 mt-2">
                          Duration: {interaction.duration} | Easing: {interaction.easing}
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {activeTab === 'assets' && (
                  <div className="space-y-3">
                    {result.visual_assets.map((asset: any, idx: number) => (
                      <div key={idx} className="bg-white rounded-lg p-4 border">
                        <div className="font-semibold text-gray-900 mb-1">
                          {asset.asset_type} for {asset.component}
                        </div>
                        <div className="text-sm text-gray-600 mb-2">{asset.description}</div>
                        <div className="bg-gray-100 rounded-lg p-3">
                          <div className="text-xs font-semibold text-gray-500 mb-1">AI Prompt</div>
                          <p className="text-xs text-gray-700">{asset.prompt}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </>
          ) : (
            <div className="flex flex-col items-center justify-center h-full text-gray-400">
              <div className="text-6xl mb-4">🎨</div>
              <div className="text-lg font-medium">选择风格和参数</div>
              <div className="text-sm">点击生成按钮开始设计</div>
            </div>
          )}
        </Card>
      </div>
    </div>
  )
}
