/**
 * Copyright 2024 Beijing Volcano Engine Technology Co., Ltd. All Rights Reserved.
 * SPDX-license-identifier: BSD-3-Clause
 */

import React, { useState, useContext, useEffect, useCallback, useRef } from 'react';
import { message } from 'antd';
import styled from 'styled-components';
import {
  MediaType,
  onUserJoinedEvent,
  onUserLeaveEvent,
  PlayerEvent,
  AutoPlayFailedEvent,
} from '@volcengine/rtc';
import { ControlBar, AutoPlayModal } from '../../modules';
import { Context } from '../../context';

import RTCComponent from '../../sdk/rtc-component';
import { RTCClient } from '../../app-interfaces';
import { streamOptions } from './constant';
import config from '../../config';
import MediaPlayer from '../../components/MediaPlayer';
import { removeLoginInfo } from '../../utils';

const Container = styled.div`
  width: 100%;
  height: 100%;
  display: flex;
  flex-wrap: wrap;
  padding: 8px;
  gap: 8px;
`;

const Item = styled.div`
  flex: 1;
  width: calc(50% - 8px);
  min-width: calc(50% - 8px);
  max-width: calc(50% - 8px);
  height: calc(50% - 8px);
  position: relative;
`;

const StatsPanel = styled.div`
  position: fixed;
  top: 48px;
  right: 12px;
  background: rgba(0, 0, 0, 0.75);
  color: #fff;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 12px;
  line-height: 1.8;
  z-index: 9999;
  min-width: 220px;
  max-height: calc(100vh - 120px);
  overflow-y: auto;
  backdrop-filter: blur(6px);
  cursor: pointer;
  user-select: none;
`;

const StatsTitle = styled.div`
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 6px;
  padding-bottom: 4px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
`;

const StatsSection = styled.div`
  margin-top: 8px;
`;

const StatsSectionTitle = styled.div`
  font-weight: 500;
  color: #4fc3f7;
  margin-bottom: 2px;
`;

const StatsRow = styled.div`
  display: flex;
  justify-content: space-between;
  gap: 12px;
`;

const SubtitleOverlay = styled.div`
  position: fixed;
  top: calc(50% + 30px);
  left: 40%;
  transform: translateX(-50%);
  width: 92%;
  max-width: 1100px;
  max-height: 40%;
  overflow-y: auto;
  background: rgba(0, 0, 0, 0.7);
  color: #fff;
  border-radius: 10px;
  padding: 12px 20px;
  z-index: 9999;
  backdrop-filter: blur(8px);
  display: flex;
  flex-direction: column;
  gap: 6px;
`;

const SubtitleLine = styled.div<{ $isUser: boolean }>`
  font-size: 15px;
  line-height: 1.6;
  word-break: break-word;
  text-align: ${p => (p.$isUser ? 'right' : 'left')};
  color: ${p => (p.$isUser ? '#90caf9' : '#fff')};
`;

const SubtitleRoleTag = styled.span<{ $isUser: boolean }>`
  font-size: 11px;
  font-weight: 600;
  color: ${p => (p.$isUser ? '#42a5f5' : '#66bb6a')};
  margin-right: 6px;
`;

const Meeting: React.FC<Record<string, unknown>> = () => {
  const { roomId, userId, setJoin, setJoinFailReason } = useContext(Context);
  const [isMicOn, setMicOn] = useState<boolean>(true);
  const [isVideoOn, setVideoOn] = useState<boolean>(true);
  const rtc = useRef<RTCClient>();
  const [autoPlayFailUser, setAutoPlayFailUser] = useState<string[]>([]);
  const playStatus = useRef<{ [key: string]: { audio: boolean; video: boolean } }>({});
  const autoPlayFailUserdRef = useRef<string[]>([]);

  const [showStats, setShowStats] = useState<boolean>(true);
  const [localStats, setLocalStats] = useState<any>(null);
  const [remoteStats, setRemoteStats] = useState<any>(null);

  const SPEAK_THRESHOLD = 10;
  const SILENCE_DEBOUNCE = 5;
  const latencyStateRef = useRef<'idle' | 'speaking' | 'waiting'>('idle');
  const speechEndTimeRef = useRef<number>(0);
  const silenceCountRef = useRef<number>(0);
  const [currentLatency, setCurrentLatency] = useState<number | null>(null);
  const [latencyHistory, setLatencyHistory] = useState<number[]>([]);
  const [voiceState, setVoiceState] = useState<string>('空闲');
  const latencyRecordsRef = useRef<{ index: number; timestamp: string; latency_ms: number }[]>(
    (() => {
      try {
        const saved = localStorage.getItem('latency_records');
        return saved ? JSON.parse(saved) : [];
      } catch { return []; }
    })()
  );

  interface SubtitleTurn {
    role: 'user' | 'ai';
    text: string;
    roundId: number;
    definite: boolean;
    timestamp: string;
  }
  const [subtitleTurns, setSubtitleTurns] = useState<SubtitleTurn[]>([]);
  const [showChat, setShowChat] = useState<boolean>(true);
  const subtitleRef = useRef<HTMLDivElement>(null);

  const [remoteStreams, setRemoteStreams] = useState<{
    [key: string]: {
      playerComp: React.ReactNode;
    };
  }>({});

  const leaveRoom = useCallback(
    (refresh: boolean) => {
      if (!rtc.current) return;

      // off the event
      rtc.current.removeEventListener();

      rtc.current.leave();
      if (!refresh) {
        setJoin(false);
        removeLoginInfo();
      }

      setAutoPlayFailUser([]);
      setJoinFailReason('');
    },
    [rtc, setJoin]
  );

  /**
   * @brief call leaveRoom function when the browser window closes or refreshes
   */
  const leaveFunc = () => {
    leaveRoom(true);
    sessionStorage.setItem('store', JSON.stringify({ test: new Date().toString() }));
  };
  useEffect(() => {
    window.addEventListener('pagehide', leaveFunc);
    return () => {
      leaveRoom(true);
      window.removeEventListener('pagehide', leaveFunc);
    };
  }, [leaveRoom]);

  const handleUserPublishStream = useCallback(
    (stream: { userId: string; mediaType: MediaType }) => {
      const userId = stream.userId;
      if (stream.mediaType & MediaType.VIDEO) {
        if (remoteStreams[userId]) {
          rtc.current?.setRemoteVideoPlayer(userId, `remoteStream_${userId}`);
        }
      }
    },
    [remoteStreams]
  );

  /**
   * @brief remove stream & update remote streams list
   * @param {Event} event
   */
  const handleUserUnpublishStream = (event: { userId: string; mediaType: MediaType }) => {
    const { userId, mediaType } = event;

    if (mediaType & MediaType.VIDEO) {
      rtc.current?.setRemoteVideoPlayer(userId, undefined);
    }
  };

  const handleUserStartVideoCapture = (event: { userId: string }) => {
    const { userId } = event;

    if (remoteStreams[userId]) {
      rtc.current?.setRemoteVideoPlayer(userId, `remoteStream_${userId}`);
    }
  };

  /**
   * Remove the user specified from the room in the local and clear the unused dom
   * @param {*} event
   */
  const handleUserStopVideoCapture = (event: { userId: string }) => {
    const { userId } = event;

    rtc.current?.setRemoteVideoPlayer(userId, undefined);
  };

  const handleUserJoin = (e: onUserJoinedEvent) => {
    console.log('handleUserJoin', e);

    const { userInfo } = e;
    const remoteUserId = userInfo.userId;

    if (Object.keys(remoteStreams).length < 3) {
      if (remoteStreams[remoteUserId]) return;
      remoteStreams[remoteUserId] = {
        playerComp: <MediaPlayer userId={remoteUserId} />,
      };

      setRemoteStreams({
        ...remoteStreams,
      });
    }
  };

  useEffect(() => {
    const streams = Object.keys(remoteStreams);
    const _autoPlayFailUser = autoPlayFailUser.filter(
      (item) => streams.findIndex((stream) => stream === item) !== -1
    );
    setAutoPlayFailUser([..._autoPlayFailUser]);
  }, [remoteStreams]);

  const handleUserLeave = (e: onUserLeaveEvent) => {
    const { userInfo } = e;
    const remoteUserId = userInfo.userId;
    if (remoteStreams[remoteUserId]) {
      delete remoteStreams[remoteUserId];
    }
    setRemoteStreams({
      ...remoteStreams,
    });
  };

  useEffect(() => {
    (async () => {
      if (!roomId || !userId || !rtc.current) return;
      // rtc.current.bindEngineEvents();

      let token = null;
      config.tokens.forEach((item) => {
        if (item.userId === userId) {
          token = item.token;
        }
      });

      rtc.current
        .join((token as any) || null, roomId, userId)
        .then(() =>
          rtc?.current?.createLocalStream(userId, (res: any) => {
            const { code, msg } = res;
            if (code === -1) {
              if (window.confirm(`${msg}, 是否跳转排查文档?`)) {
                window.location.href = 'https://www.volcengine.com/docs/6348/1356355';
              } 
              setMicOn(false);
              setVideoOn(false);
            }
          })
        )
        .catch((err: any) => {
          console.log('err', err);
          leaveRoom(false);
          setJoinFailReason(JSON.stringify(err));
        });
    })();
  }, [roomId, userId, rtc]);

  const changeMicState = useCallback((): void => {
    if (!rtc.current) return;
    rtc.current.changeAudioState(!isMicOn);
    setMicOn(!isMicOn);
  }, [isMicOn, rtc]);

  const changeVideoState = useCallback((): void => {
    if (!rtc.current) return;
    rtc.current.changeVideoState(!isVideoOn);
    setVideoOn(!isVideoOn);
  }, [isVideoOn, rtc]);

  const handleEventError = (e: any, VERTC: any) => {
    if (e.errorCode === VERTC.ErrorCode.DUPLICATE_LOGIN) {
      message.error('你的账号被其他人顶下线了');
      leaveRoom(false);
    }
  };

  const handleAutoPlayFail = (event: AutoPlayFailedEvent) => {
    console.log('handleAutoPlayFail', event.userId, event);
    const { userId, kind } = event;

    let playUser = playStatus.current?.[userId] || {};
    playUser = { ...playUser, [kind]: false };
    playStatus.current[userId] = playUser;

    addFailUser(userId);
  };

  const addFailUser = (userId: string) => {
    const index = autoPlayFailUser.findIndex((item) => item === userId);
    if (index === -1) {
      autoPlayFailUser.push(userId);
    }
    setAutoPlayFailUser([...autoPlayFailUser]);
  };

  const playerFail = (params: { type: 'audio' | 'video'; userId: string }) => {
    const { type, userId } = params;
    let playUser = playStatus.current?.[userId] || {};

    console.log('pause', event);

    playUser = { ...playUser, [type]: false };

    const { audio, video } = playUser;

    if (audio === false || video === false) {
      addFailUser(userId);
    }
  };

  const handlePlayerEvent = (event: PlayerEvent) => {
    const { userId, rawEvent, type } = event;

    console.log('handlePlayerEvent', event, userId, type, rawEvent.type);

    let playUser = playStatus.current?.[userId] || {};

    if (!playStatus.current) return;

    if (rawEvent.type === 'playing') {
      playUser = { ...playUser, [type]: true };
      const { audio, video } = playUser;
      if (audio !== false && video !== false) {
        const _autoPlayFailUser = autoPlayFailUserdRef.current.filter((item) => item !== userId);
        setAutoPlayFailUser([..._autoPlayFailUser]);
      }
    } else if (rawEvent.type === 'pause') {
      playerFail({ userId, type });
    }

    playStatus.current[userId] = playUser;
    console.log('playStatusplayStatusplayStatus', playStatus);
  };

  const handleAutoPlay = () => {
    const users: string[] = autoPlayFailUser;
    console.log('handleAutoPlay autoPlayFailUser', autoPlayFailUser);
    if (users && users.length) {
      users.forEach((user) => {
        rtc.current?.engine.play(user);
      });
    }
    setAutoPlayFailUser([]);
  };

  const handleLocalStreamStats = useCallback((stats: any) => {
    setLocalStats(stats);
  }, []);

  const handleRemoteStreamStats = useCallback((stats: any) => {
    setRemoteStats(stats);
  }, []);

  const handleLocalAudioReport = useCallback((reports: any) => {
    const infos = reports?.audioPropertiesInfos || reports;
    if (!infos || !infos.length) return;
    const volume = infos[0]?.audioPropertiesInfo?.linearVolume ?? 0;

    if (volume > SPEAK_THRESHOLD) {
      silenceCountRef.current = 0;
      if (latencyStateRef.current !== 'speaking') {
        latencyStateRef.current = 'speaking';
        setVoiceState('用户说话中...');
      }
    } else if (latencyStateRef.current === 'speaking') {
      silenceCountRef.current += 1;
      if (silenceCountRef.current >= SILENCE_DEBOUNCE) {
        latencyStateRef.current = 'waiting';
        speechEndTimeRef.current = performance.now();
        silenceCountRef.current = 0;
        setVoiceState('等待 AI 响应...');
      }
    }
  }, []);

  const handleRemoteAudioReport = useCallback((reports: any) => {
    if (latencyStateRef.current !== 'waiting') return;
    const infos = reports?.audioPropertiesInfos || reports;
    if (!infos || !infos.length) return;

    for (const item of infos) {
      const volume = item?.audioPropertiesInfo?.linearVolume ?? 0;
      if (volume > SPEAK_THRESHOLD) {
        const latency = Math.round(performance.now() - speechEndTimeRef.current);
        latencyStateRef.current = 'idle';
        setCurrentLatency(latency);
        setLatencyHistory(prev => [...prev.slice(-19), latency]);
        setVoiceState('AI 回复中');

        const record = {
          index: latencyRecordsRef.current.length + 1,
          timestamp: new Date().toISOString(),
          latency_ms: latency,
        };
        latencyRecordsRef.current.push(record);
        try {
          localStorage.setItem('latency_records', JSON.stringify(latencyRecordsRef.current));
        } catch (e) {
          console.warn('localStorage write failed', e);
        }
        console.log(`[首帧延迟] ${latency}ms`, record);
        break;
      }
    }
  }, []);

  const handleSubtitleMessage = useCallback((msg: any) => {
    const items = msg?.data || msg?.Data || [];
    if (!items.length) return;

    setSubtitleTurns(prev => {
      const next = [...prev];
      for (const item of items) {
        const uid = item.userId || item.uid || '';
        const text = item.text || item.Text || '';
        const definite = item.definite ?? false;
        const paragraph = item.paragraph ?? false;
        const roundId = item.roundId ?? item.sequence ?? 0;
        const role: 'user' | 'ai' = (uid && uid !== userId) ? 'ai' : 'user';

        const last = next.length > 0 ? next[next.length - 1] : null;
        const sameRole = last && last.role === role;
        const canMerge = sameRole && (role === 'ai' || !last.definite);

        if (last && canMerge) {
          if (role === 'user') {
            last.text = text;
          } else {
            if (text === last.text || last.text.endsWith(text)) {
              // skip duplicate
            } else if (text.length > last.text.length && text.startsWith(last.text.slice(0, Math.min(10, last.text.length)))) {
              last.text = text;
            } else {
              last.text = last.text + text;
            }
          }
          last.roundId = roundId;
          last.definite = role === 'user' ? (definite || paragraph) : false;
          last.timestamp = new Date().toLocaleTimeString();
        } else {
          next.push({
            role,
            text,
            roundId,
            definite: role === 'user' ? (definite || paragraph) : false,
            timestamp: new Date().toLocaleTimeString(),
          });
        }
      }
      return next;
    });
  }, [userId]);

  useEffect(() => {
    if (subtitleRef.current) {
      subtitleRef.current.scrollTop = subtitleRef.current.scrollHeight;
    }
  }, [subtitleTurns]);

  const exportLatencyCSV = useCallback(() => {
    const records = latencyRecordsRef.current;
    if (!records.length) {
      message.warning('暂无延迟数据');
      return;
    }
    const header = '序号,时间,延迟(ms)\n';
    const rows = records.map(r => `${r.index},${r.timestamp},${r.latency_ms}`).join('\n');
    const blob = new Blob([header + rows], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `latency_${new Date().toISOString().slice(0, 19).replace(/[:-]/g, '')}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }, []);

  const clearLatencyRecords = useCallback(() => {
    latencyRecordsRef.current = [];
    setLatencyHistory([]);
    setCurrentLatency(null);
    localStorage.removeItem('latency_records');
    message.success('延迟记录已清空');
  }, []);

  const avgLatency = latencyHistory.length
    ? Math.round(latencyHistory.reduce((a, b) => a + b, 0) / latencyHistory.length)
    : null;
  const minLatency = latencyHistory.length ? Math.min(...latencyHistory) : null;
  const maxLatency = latencyHistory.length ? Math.max(...latencyHistory) : null;

  const renderStatsValue = (label: string, value: any, unit = '') => (
    <StatsRow key={label}>
      <span style={{ color: '#aaa' }}>{label}</span>
      <span>{value !== undefined && value !== null ? `${value}${unit}` : '-'}</span>
    </StatsRow>
  );

  useEffect(() => {
    autoPlayFailUserdRef.current = autoPlayFailUser;
  }, [autoPlayFailUser]);

  return (
    <>
      <RTCComponent
        onRef={(ref: any) => (rtc.current = ref)}
        config={{
          ...config,
          roomId,
          uid: '',
        }}
        streamOptions={streamOptions}
        handleUserPublishStream={handleUserPublishStream}
        handleUserUnpublishStream={handleUserUnpublishStream}
        handleUserStartVideoCapture={handleUserStartVideoCapture}
        handleUserStopVideoCapture={handleUserStopVideoCapture}
        handleUserJoin={handleUserJoin}
        handleUserLeave={handleUserLeave}
        handleEventError={handleEventError}
        handleAutoPlayFail={handleAutoPlayFail}
        handlePlayerEvent={handlePlayerEvent}
        handleLocalStreamStats={handleLocalStreamStats}
        handleRemoteStreamStats={handleRemoteStreamStats}
        handleLocalAudioReport={handleLocalAudioReport}
        handleRemoteAudioReport={handleRemoteAudioReport}
        handleSubtitleMessage={handleSubtitleMessage}
      />
      <Container>
        <Item>
          <div
            style={{
              width: '100%',
              height: '100%',
              position: 'relative',
              background: '#000',
            }}
            id={'local-player'}
          >
            <span
              style={{
                color: '#fff',
                position: 'absolute',
                bottom: 0,
                right: 0,
                zIndex: 1000,
                maxWidth: 120,
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap',
              }}
            >
              {userId}
            </span>
          </div>
        </Item>
        {Object.keys(remoteStreams)?.map((key) => {
          const Comp = remoteStreams[key].playerComp;
          return <Item key={key}>{Comp}</Item>;
        })}
      </Container>
      {showChat && subtitleTurns.length > 0 && (
        <SubtitleOverlay ref={subtitleRef}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 2 }}>
            <span style={{ fontSize: 11, color: '#666' }}>对话字幕</span>
            <div style={{ display: 'flex', gap: 10 }}>
              <span
                onClick={() => setSubtitleTurns([])}
                style={{ cursor: 'pointer', fontSize: 11, color: '#666' }}
              >
                清空
              </span>
              <span
                onClick={() => setShowChat(false)}
                style={{ cursor: 'pointer', fontSize: 11, color: '#666' }}
              >
                隐藏
              </span>
            </div>
          </div>
          {subtitleTurns.slice(-6).map((turn, i) => (
            <SubtitleLine key={`${turn.role}-${turn.roundId}`} $isUser={turn.role === 'user'}>
              <SubtitleRoleTag $isUser={turn.role === 'user'}>
                {turn.role === 'user' ? '我' : 'AI'}
              </SubtitleRoleTag>
              {turn.text}
              {!turn.definite && <span style={{ color: '#ffa726', fontSize: 12 }}> ...</span>}
            </SubtitleLine>
          ))}
        </SubtitleOverlay>
      )}
      {!showChat && (
        <div
          onClick={() => setShowChat(true)}
          style={{
            position: 'fixed',
            top: 'calc(50% + 20px)',
            left: '50%',
            transform: 'translateX(-50%)',
            background: 'rgba(0,0,0,0.5)',
            color: '#4fc3f7',
            padding: '4px 16px',
            borderRadius: 6,
            fontSize: 12,
            cursor: 'pointer',
            zIndex: 9999,
          }}
        >
          显示字幕
        </div>
      )}
      {showStats && (
        <StatsPanel onClick={() => setShowStats(false)}>
          <StatsTitle>语音对话延迟监控</StatsTitle>

          <StatsSection>
            <StatsSectionTitle>状态</StatsSectionTitle>
            <div style={{ fontSize: 13, color: '#e0e0e0' }}>{voiceState}</div>
          </StatsSection>

          <StatsSection>
            <StatsSectionTitle>首帧音频响应延迟</StatsSectionTitle>
            <div style={{
              fontSize: 28,
              fontWeight: 700,
              color: currentLatency !== null
                ? (currentLatency < 1000 ? '#66bb6a' : currentLatency < 2000 ? '#ffa726' : '#ef5350')
                : '#666',
              margin: '4px 0',
            }}>
              {currentLatency !== null ? `${currentLatency} ms` : '-- ms'}
            </div>
          </StatsSection>

          {latencyHistory.length > 0 && (
            <StatsSection>
              <StatsSectionTitle>统计 (最近 {latencyHistory.length} 次)</StatsSectionTitle>
              {renderStatsValue('平均', avgLatency, ' ms')}
              {renderStatsValue('最小', minLatency, ' ms')}
              {renderStatsValue('最大', maxLatency, ' ms')}
            </StatsSection>
          )}

          {latencyHistory.length > 0 && (
            <StatsSection>
              <StatsSectionTitle>历史记录</StatsSectionTitle>
              <div style={{ maxHeight: 120, overflowY: 'auto', fontSize: 11 }}>
                {[...latencyHistory].reverse().map((l, i) => (
                  <div key={i} style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    color: l < 1000 ? '#66bb6a' : l < 2000 ? '#ffa726' : '#ef5350',
                  }}>
                    <span style={{ color: '#666' }}>#{latencyHistory.length - i}</span>
                    <span>{l} ms</span>
                  </div>
                ))}
              </div>
            </StatsSection>
          )}

          <StatsSection>
            <StatsSectionTitle>RTC 通道质量</StatsSectionTitle>
            {remoteStats?.audioStats && (
              <>
                {renderStatsValue('音频端到端延迟', remoteStats.audioStats.e2eDelay, ' ms')}
                {renderStatsValue('音频丢包率', remoteStats.audioStats.audioLossRate, '%')}
              </>
            )}
            {remoteStats?.videoStats && (
              <>
                {renderStatsValue('视频端到端延迟', remoteStats.videoStats.e2eDelay, ' ms')}
                {renderStatsValue('视频丢包率', remoteStats.videoStats.videoLossRate, '%')}
              </>
            )}
            {!remoteStats && (
              <div style={{ color: '#666' }}>等待数据...</div>
            )}
          </StatsSection>

          <StatsSection>
            <div style={{ display: 'flex', gap: 8, marginTop: 4 }}>
              <button
                onClick={(e) => { e.stopPropagation(); exportLatencyCSV(); }}
                style={{
                  flex: 1,
                  padding: '5px 0',
                  background: '#4fc3f7',
                  color: '#000',
                  border: 'none',
                  borderRadius: 4,
                  fontSize: 12,
                  fontWeight: 600,
                  cursor: 'pointer',
                }}
              >
                导出 CSV
              </button>
              <button
                onClick={(e) => { e.stopPropagation(); clearLatencyRecords(); }}
                style={{
                  flex: 1,
                  padding: '5px 0',
                  background: 'rgba(255,255,255,0.15)',
                  color: '#aaa',
                  border: 'none',
                  borderRadius: 4,
                  fontSize: 12,
                  cursor: 'pointer',
                }}
              >
                清空记录
              </button>
            </div>
            <div style={{ color: '#555', fontSize: 10, marginTop: 6, textAlign: 'center' }}>
              共 {latencyRecordsRef.current.length} 条记录 (自动保存至 localStorage)
            </div>
          </StatsSection>
          <div style={{ color: '#666', fontSize: 11, marginTop: 8, textAlign: 'center' }}>
            点击面板可隐藏
          </div>
        </StatsPanel>
      )}
      {!showStats && (
        <div
          onClick={() => setShowStats(true)}
          style={{
            position: 'fixed',
            top: 48,
            right: 12,
            background: 'rgba(0,0,0,0.6)',
            color: '#4fc3f7',
            padding: '4px 12px',
            borderRadius: 6,
            fontSize: 12,
            cursor: 'pointer',
            zIndex: 9999,
          }}
        >
          显示延迟监控
        </div>
      )}
      <ControlBar
        RClient={rtc}
        systemConf={[
          {
            moduleName: 'DividerModule',
            moduleProps: {
              width: 2,
              height: 32,
              marginL: 20,
            },
            visible: true,
          },
          {
            moduleName: 'HangUpModule',
            moduleProps: {
              changeHooks: () => {
                leaveRoom(false);
              },
            },
          },
        ]}
        moduleConf={[
          {
            moduleName: 'MicoPhoneControlModule',
            moduleProps: {
              changeHooks: () => changeMicState(),
              isMicOn,
            },
            visible: true,
          },
          {
            moduleName: 'VideoControlModule',
            moduleProps: {
              changeHooks: () => changeVideoState(),
              isVideoOn,
            },
            visible: true,
          },
        ]}
      />
      <AutoPlayModal handleAutoPlay={handleAutoPlay} autoPlayFailUser={autoPlayFailUser} />
    </>
  );
};

export default Meeting;
