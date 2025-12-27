import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { 
  CheckCircle, XCircle, Activity, Clock, TrendingUp, 
  Package, AlertTriangle, RefreshCw, Play, Pause,
  BarChart3, Zap, Target, Shield
} from 'lucide-react';

const API_URL = 'http://localhost:8000';

function App() {
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState('');
  const [dashboard, setDashboard] = useState(null);
  const [lastResult, setLastResult] = useState(null);
  const [isAutoMode, setIsAutoMode] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const fetchProducts = useCallback(async () => {
    try {
      const res = await axios.get(`${API_URL}/products`);
      setProducts(res.data);
      if (res.data.length > 0 && !selectedProduct) {
        setSelectedProduct(res.data[0].code);
      }
    } catch (error) {
      console.error('Ürünler yüklenemedi:', error);
    }
  }, [selectedProduct]);

  const fetchDashboard = useCallback(async () => {
    try {
      const res = await axios.get(`${API_URL}/dashboard`);
      setDashboard(res.data);
    } catch (error) {
      console.error('Dashboard yüklenemedi:', error);
    }
  }, []);

  const runSimulation = useCallback(async () => {
    if (!selectedProduct || isLoading) return;
    
    setIsLoading(true);
    try {
      const res = await axios.post(`${API_URL}/simulate?product_code=${selectedProduct}`);
      setLastResult(res.data);
      await fetchDashboard();
    } catch (error) {
      console.error('Simülasyon hatası:', error);
    } finally {
      setIsLoading(false);
    }
  }, [selectedProduct, isLoading, fetchDashboard]);

  const runBatchSimulation = async () => {
    setIsLoading(true);
    try {
      await axios.post(`${API_URL}/batch-simulate?count=25`);
      await fetchDashboard();
    } catch (error) {
      console.error('Toplu simülasyon hatası:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const clearHistory = async () => {
    try {
      await axios.delete(`${API_URL}/history`);
      setDashboard(null);
      setLastResult(null);
      await fetchDashboard();
    } catch (error) {
      console.error('Geçmiş temizlenemedi:', error);
    }
  };

  useEffect(() => {
    fetchProducts();
    fetchDashboard();
  }, [fetchProducts, fetchDashboard]);

  useEffect(() => {
    let interval;
    if (isAutoMode) {
      interval = setInterval(() => {
        runSimulation();
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [isAutoMode, runSimulation]);

  const getStatusColor = (status) => {
    return status === 'PASSED' ? 'text-green-500' : 'text-red-500';
  };

  const getStatusBg = (status) => {
    return status === 'PASSED' ? 'bg-green-500' : 'bg-red-500';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Header */}
      <header className="bg-slate-800/50 backdrop-blur-sm border-b border-slate-700">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center">
                <Target className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">VisionQC</h1>
                <p className="text-sm text-slate-400">Yapay Zeka Destekli Kalite Kontrol</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-sm flex items-center gap-1">
                <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                Sistem Aktif
              </span>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm">Toplam Kontrol</p>
                <p className="text-3xl font-bold text-white">{dashboard?.total_inspections || 0}</p>
              </div>
              <div className="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-blue-400" />
              </div>
            </div>
          </div>

          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm">Geçti</p>
                <p className="text-3xl font-bold text-green-400">{dashboard?.passed || 0}</p>
              </div>
              <div className="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center">
                <CheckCircle className="w-6 h-6 text-green-400" />
              </div>
            </div>
          </div>

          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm">Kaldı</p>
                <p className="text-3xl font-bold text-red-400">{dashboard?.failed || 0}</p>
              </div>
              <div className="w-12 h-12 bg-red-500/20 rounded-lg flex items-center justify-center">
                <XCircle className="w-6 h-6 text-red-400" />
              </div>
            </div>
          </div>

          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm">Başarı Oranı</p>
                <p className="text-3xl font-bold text-white">{dashboard?.pass_rate?.toFixed(1) || 0}%</p>
              </div>
              <div className="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-purple-400" />
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Control Panel */}
          <div className="lg:col-span-1 space-y-4">
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-5 border border-slate-700">
              <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <Package className="w-5 h-5 text-blue-400" />
                Kontrol Paneli
              </h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm text-slate-400 mb-2">Ürün Seçimi</label>
                  <select
                    value={selectedProduct}
                    onChange={(e) => setSelectedProduct(e.target.value)}
                    className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    {products.map((p) => (
                      <option key={p.code} value={p.code}>
                        {p.code} - {p.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="grid grid-cols-2 gap-2">
                  <button
                    onClick={runSimulation}
                    disabled={isLoading}
                    className="flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-medium py-2.5 px-4 rounded-lg transition-colors"
                  >
                    {isLoading ? (
                      <RefreshCw className="w-4 h-4 animate-spin" />
                    ) : (
                      <Zap className="w-4 h-4" />
                    )}
                    Tek Kontrol
                  </button>

                  <button
                    onClick={() => setIsAutoMode(!isAutoMode)}
                    className={`flex items-center justify-center gap-2 font-medium py-2.5 px-4 rounded-lg transition-colors ${
                      isAutoMode 
                        ? 'bg-orange-600 hover:bg-orange-700 text-white' 
                        : 'bg-slate-700 hover:bg-slate-600 text-white'
                    }`}
                  >
                    {isAutoMode ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                    {isAutoMode ? 'Durdur' : 'Oto Mod'}
                  </button>
                </div>

                <button
                  onClick={runBatchSimulation}
                  disabled={isLoading}
                  className="w-full flex items-center justify-center gap-2 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 text-white font-medium py-2.5 px-4 rounded-lg transition-colors"
                >
                  <Activity className="w-4 h-4" />
                  Toplu Simülasyon (25 Ürün)
                </button>

                <button
                  onClick={clearHistory}
                  className="w-full flex items-center justify-center gap-2 bg-slate-700 hover:bg-slate-600 text-slate-300 font-medium py-2.5 px-4 rounded-lg transition-colors"
                >
                  <RefreshCw className="w-4 h-4" />
                  Geçmişi Temizle
                </button>
              </div>
            </div>

            {/* Selected Product Specs */}
            {selectedProduct && products.length > 0 && (
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-5 border border-slate-700">
                <h3 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
                  <Shield className="w-5 h-5 text-green-400" />
                  Ürün Spesifikasyonu
                </h3>
                {(() => {
                  const product = products.find(p => p.code === selectedProduct);
                  if (!product) return null;
                  return (
                    <div className="space-y-2">
                      <p className="text-sm text-slate-400">{product.name}</p>
                      <div className="grid grid-cols-3 gap-2 text-center">
                        <div className="bg-slate-700/50 rounded-lg p-2">
                          <p className="text-xs text-slate-400">Uzunluk</p>
                          <p className="text-white font-semibold">{product.nominal.length}mm</p>
                          <p className="text-xs text-blue-400">±{product.tolerance.length}</p>
                        </div>
                        <div className="bg-slate-700/50 rounded-lg p-2">
                          <p className="text-xs text-slate-400">Genişlik</p>
                          <p className="text-white font-semibold">{product.nominal.width}mm</p>
                          <p className="text-xs text-blue-400">±{product.tolerance.width}</p>
                        </div>
                        <div className="bg-slate-700/50 rounded-lg p-2">
                          <p className="text-xs text-slate-400">Yükseklik</p>
                          <p className="text-white font-semibold">{product.nominal.height}mm</p>
                          <p className="text-xs text-blue-400">±{product.tolerance.height}</p>
                        </div>
                      </div>
                    </div>
                  );
                })()}
              </div>
            )}
          </div>

          {/* Last Result */}
          <div className="lg:col-span-1">
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-5 border border-slate-700 h-full">
              <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <Activity className="w-5 h-5 text-purple-400" />
                Son Kontrol Sonucu
              </h2>

              {lastResult ? (
                <div className="space-y-4">
                  <div className={`text-center py-6 rounded-xl ${lastResult.status === 'PASSED' ? 'bg-green-500/20' : 'bg-red-500/20'}`}>
                    <div className={`text-5xl font-bold ${getStatusColor(lastResult.status)}`}>
                      {lastResult.status === 'PASSED' ? 'GEÇTİ' : 'KALDI'}
                    </div>
                    <p className="text-slate-400 mt-2">Güven: %{lastResult.confidence}</p>
                  </div>

                  <div className="bg-slate-700/30 rounded-lg p-4">
                    <p className="text-sm text-slate-400 mb-2">Ürün: {lastResult.product_name}</p>
                    <p className="text-sm text-slate-400 mb-3">Kod: {lastResult.product_code}</p>
                    
                    <div className="space-y-2">
                      {['length', 'width', 'height'].map((dim) => {
                        const isOutOfTolerance = Math.abs(lastResult.deviations[dim]) > lastResult.tolerance[dim];
                        const label = dim === 'length' ? 'Uzunluk' : dim === 'width' ? 'Genişlik' : 'Yükseklik';
                        return (
                          <div key={dim} className={`flex items-center justify-between p-2 rounded ${isOutOfTolerance ? 'bg-red-500/20' : 'bg-green-500/10'}`}>
                            <span className="text-slate-300">{label}</span>
                            <div className="text-right">
                              <span className={`font-mono ${isOutOfTolerance ? 'text-red-400' : 'text-green-400'}`}>
                                {lastResult.measurements[dim]}mm
                              </span>
                              <span className="text-xs text-slate-500 ml-2">
                                ({lastResult.deviations[dim] >= 0 ? '+' : ''}{lastResult.deviations[dim]})
                              </span>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>

                  <div className="flex items-center justify-between text-sm text-slate-400">
                    <span className="flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      {lastResult.processing_time_ms}ms
                    </span>
                    <span>{new Date(lastResult.timestamp).toLocaleTimeString('tr-TR')}</span>
                  </div>

                  {lastResult.issues.length > 0 && (
                    <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-3">
                      <p className="text-red-400 text-sm font-medium flex items-center gap-1 mb-1">
                        <AlertTriangle className="w-4 h-4" />
                        Tespit Edilen Sorunlar
                      </p>
                      <ul className="text-sm text-red-300 space-y-1">
                        {lastResult.issues.map((issue, i) => (
                          <li key={i}>• {issue}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ) : (
                <div className="h-64 flex items-center justify-center text-slate-500">
                  <div className="text-center">
                    <Activity className="w-12 h-12 mx-auto mb-2 opacity-50" />
                    <p>Henüz kontrol yapılmadı</p>
                    <p className="text-sm">Başlamak için "Tek Kontrol" butonuna tıklayın</p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Recent Inspections */}
          <div className="lg:col-span-1">
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-5 border border-slate-700 h-full">
              <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <Clock className="w-5 h-5 text-orange-400" />
                Son Kontroller
              </h2>

              <div className="space-y-2 max-h-[500px] overflow-y-auto pr-2">
                {dashboard?.recent_inspections?.length > 0 ? (
                  dashboard.recent_inspections.map((inspection, index) => (
                    <div
                      key={index}
                      className="flex items-center justify-between bg-slate-700/30 rounded-lg p-3 hover:bg-slate-700/50 transition-colors"
                    >
                      <div className="flex items-center gap-3">
                        <div className={`w-3 h-3 rounded-full ${getStatusBg(inspection.status)}`}></div>
                        <div>
                          <p className="text-white text-sm font-medium">{inspection.product_code}</p>
                          <p className="text-slate-400 text-xs">
                            {new Date(inspection.timestamp).toLocaleTimeString('tr-TR')}
                          </p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className={`text-sm font-semibold ${getStatusColor(inspection.status)}`}>
                          {inspection.status === 'PASSED' ? 'GEÇTİ' : 'KALDI'}
                        </p>
                        <p className="text-xs text-slate-400">{inspection.processing_time_ms}ms</p>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="h-32 flex items-center justify-center text-slate-500">
                    <p>Kontrol geçmişi boş</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Footer Info */}
        <div className="mt-6 text-center text-slate-500 text-sm">
          <p>VisionQC Demo - Yapay Zeka ile Yerel Dönüşüm Atölyesi 2025</p>
          <p className="mt-1">Problem 1: Ölçüsel Sapmaların Gözden Kaçması - Çözüm Prototipi</p>
        </div>
      </main>
    </div>
  );
}

export default App;
