import { Pressable, StyleSheet, View } from 'react-native';

import { ClayGloss } from '@/components/ClayGloss';
import { Icon, type IconName } from '@/components/Icon';
import { Txt } from '@/components/Txt';
import { clay, color, radius, rhythm, size } from '@/theme/tokens';

/**
 * §7.7 — yüzen sekme çubuğu. REV2: merkez "+" FAB kaldırıldı (harcama ekleme
 * artık yalnız Günlük kategori satırındaki "+", favoriler ve rutinlerden
 * yapılır — bkz. app/index.tsx, favoriler.tsx, rutinler.tsx). 3 sekme çubuk
 * içinde eşit ve ortalanmış dağılır. Etiketsiz ikon YOK.
 */
export type TabKey = 'gunluk' | 'tasarruflar' | 'profil';

const SEKMELER: { key: TabKey; ad: string; ikon: IconName }[] = [
  { key: 'gunluk', ad: 'Günlük', ikon: 'gauge' },
  { key: 'tasarruflar', ad: 'Tasarruf', ikon: 'notebook' },
  { key: 'profil', ad: 'Profil', ikon: 'user' },
];

export function TabBar({
  active,
  onSelect,
}: {
  active: TabKey;
  onSelect?: (key: TabKey) => void;
}) {
  return (
    <View style={stil.alan}>
      <View style={stil.cubuk}>
        <ClayGloss />
        {SEKMELER.map((s) => {
          const aktif = s.key === active;
          const tone = aktif ? color.primaryText : color.text2;
          return (
            <Pressable
              key={s.key}
              onPress={() => onSelect?.(s.key)}
              accessibilityRole="tab"
              accessibilityLabel={`${s.ad} sekmesi`}
              accessibilityState={{ selected: aktif }}
              style={stil.sekme}>
              <View
                style={[
                  stil.ikonKab,
                  aktif && {
                    height: size.tabIconBoxHeightActive,
                    backgroundColor: color.primarySoft,
                    boxShadow: clay.sunken,
                  },
                ]}>
                <Icon name={s.ikon} size={size.icon} color={tone} />
              </View>
              <View style={{ height: rhythm.sameObject }} />
              <Txt
                role={aktif ? 'label' : 'caption'}
                tone={tone}
                numberOfLines={1}
                style={stil.sekmeEtiketi}>
                {s.ad}
              </Txt>
            </Pressable>
          );
        })}
      </View>
    </View>
  );
}

const stil = StyleSheet.create({
  alan: { height: size.tabAreaHeight },
  cubuk: {
    position: 'absolute',
    left: 0,
    right: 0,
    bottom: 0,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    height: size.tabBarHeight,
    paddingHorizontal: size.tabBarPadX,
    borderRadius: radius.pill,
    backgroundColor: color.surface,
    boxShadow: clay.raisedLg,
    overflow: 'hidden',
  },
  sekme: {
    flex: 1,
    minWidth: 0,
    height: size.tabItemHeight,
    alignItems: 'center',
    justifyContent: 'center',
  },
  ikonKab: {
    width: size.tabIconBox,
    height: size.tabIconBoxHeight,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: radius.pill,
  },
  sekmeEtiketi: { width: '100%', textAlign: 'center' },
});
